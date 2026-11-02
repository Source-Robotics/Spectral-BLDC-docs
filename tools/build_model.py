#!/usr/bin/env python3
"""Build the 3D model the landing page's viewer shows, from the driver's STEP file.

    python tools/build_model.py --step PATH

Writes docs/assets/models/spectral/: body.glb and viewer.json for docs/javascripts/gripper-viewer.js (no jaws, no
colour choice: the board is shown as it is). The board looks like the real one: black solder mask, tinned mounting
rings, cream connectors, brown ceramic capacitors, black resistors and chips with metal ends and pins, gold crystal
pads. The STEP files carry few colours (KiCad's some, SolidWorks' none), so every solid gets a material from its
component name (KiCad), its colour, and its size and shape; chip resistors and capacitors are rebuilt as clean boxes
with metal end caps, and chip pins are the low faces at a chip's edge. One mesh per material, tessellated at a
tolerance coarse enough for the web (never decimated) and compressed with gltfpack. The board is turned so that its
components point up (glTF is Y-up) and centred.

Needs cadquery's OCP (the Open CASCADE kernel), trimesh and numpy: the workspace's .venv-cad environment, not the
docs one; and Node.js for gltfpack (optional: without it the file is larger). The STEP file lives in the product
repository (STEP files/Spectral_micro_STEP.STEP); it is not copied into this one. STEPFOC-docs and Spectral-BLDC-docs
carry the same script; only OUT and DEFAULT_STEP differ.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import trimesh
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.Quantity import Quantity_Color, Quantity_TOC_sRGB
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDataStd import TDataStd_Name
from OCP.TDF import TDF_Label, TDF_LabelSequence
from OCP.TDocStd import TDocStd_Document
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS
from OCP.XCAFDoc import XCAFDoc_ColorType, XCAFDoc_DocumentTool

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "models" / "spectral"
DEFAULT_STEP = ROOT.parent.parent / "projects" / "Spectral-Micro-BLDC-controller" / "STEP files" / "Spectral_micro_STEP.STEP"
# Tessellation: the largest gap between the mesh and the true surface, and the largest angle between neighbouring
# facets of a curved face. Coarse enough for the web, and every part keeps its shape.
DEFLECTION_MM = 0.1
ANGLE_RAD = 0.5

# name: sRGB colour, metalness, roughness. Picked to match photos of the boards (black mask, ENIG/tin, JST cream).
MATERIALS = {
    "mask": ("#16181d", 0.0, 0.42),
    "ring": ("#c9cbcf", 1.0, 0.30),
    "tin": ("#c8cacd", 1.0, 0.32),
    "gold": ("#d6ad55", 1.0, 0.30),
    "silver": ("#d4d6da", 1.0, 0.22),
    "ceramic": ("#8e6243", 0.0, 0.55),
    "resistor": ("#1a1a1c", 0.0, 0.50),
    "plastic": ("#1d1e21", 0.0, 0.60),
    "cream": ("#ebe3cf", 0.0, 0.70),
    "white": ("#efefef", 0.0, 0.55),
    "led": ("#f4f1e6", 0.0, 0.30),
}
CONNECTOR_NAMES = ("S2B-", "SM04B", "-XH-", "-ZR-", "SRSS", "JST", "CONN", "PINHEADER", "PIN_HEADER")
CHIP_SIZES = ((1.0, 0.5), (1.6, 0.8), (2.0, 1.25), (3.2, 1.6), (3.2, 2.5))   # 0402, 0603, 0805, 1206, 1210 in mm
NAME_COLOUR_RULES = {   # (name fragment, STEP colour) -> material, for the vendor models of the Spectral Micro
    ("CM9V", "#404040"): "plastic", ("CM9V", "#ffcf80"): "gold",
    ("CHS-01", "#404040"): "plastic", ("CHS-01", "#c0c0c0"): "silver", ("CHS-01", None): "white",
    ("DLW21", "#404040"): "plastic", ("DLW21", "#f7e099"): "gold", ("DLW21", "#cad1ee"): "white",
    ("TPS61196", "#404040"): "plastic", ("TPS61196", "#cad1ee"): "tin", ("TPS61196", "#ffffff"): "white",
}


# ------------------------------------------------------------------ reading the STEP: solids with name and colour
def read_parts(path: Path):
    """Every solid of the STEP, placed, with the name of the component it belongs to and its colour (or None)."""
    doc = TDocStd_Document(TCollection_ExtendedString("board"))
    reader = STEPCAFControl_Reader()
    reader.SetColorMode(True)
    reader.SetNameMode(True)
    if reader.ReadFile(str(path)) != 1:
        sys.exit(f"build_model: cannot read {path}")
    reader.Transfer(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    ct = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())

    def name(lab):
        n = TDataStd_Name()
        return n.Get().ToExtString() if lab.FindAttribute(TDataStd_Name.GetID_s(), n) else ""

    def colour(shape):
        c = Quantity_Color()
        for kind in (XCAFDoc_ColorType.XCAFDoc_ColorSurf, XCAFDoc_ColorType.XCAFDoc_ColorGen):
            if ct.GetColor(shape, kind, c):
                return "#%02x%02x%02x" % tuple(round(v * 255) for v in c.Values(Quantity_TOC_sRGB))
        return None

    parts, counter = [], [0]

    def walk(lab, loc, names, instance):
        if st.IsAssembly_s(lab):
            comps = TDF_LabelSequence()
            st.GetComponents_s(lab, comps)
            for i in range(1, comps.Length() + 1):
                comp, ref = comps.Value(i), TDF_Label()
                target = ref if st.GetReferredShape_s(comp, ref) else comp
                if instance is None and len(names) == 1:
                    counter[0] += 1                     # a top-level component: one instance id for all its solids
                walk(target, loc.Multiplied(st.GetLocation_s(comp)), names + [name(target)],
                     instance if instance is not None or len(names) > 1 else counter[0])
            return
        shape = st.GetShape_s(lab)
        exp = TopExp_Explorer(shape, TopAbs_SOLID)
        while exp.More():
            solid = exp.Current()
            meaningful = [n for n in names if n and n not in ("SOLID", "COMPOUND")]
            # a solid outside any component (a SolidWorks export is one part) has no component name of its own
            parts.append(dict(solid=solid.Moved(loc), name=meaningful[-1] if meaningful and instance is not None else "",
                              colour=colour(solid) or colour(shape), instance=instance if instance is not None else -len(parts) - 1))
            exp.Next()

    free = TDF_LabelSequence()
    st.GetFreeShapes(free)
    for i in range(1, free.Length() + 1):
        walk(free.Value(i), TopLoc_Location(), [name(free.Value(i))], None)
    return parts


def faces_of(solid):
    """The solid's faces as (vertices in mm, triangles), tessellated."""
    BRepMesh_IncrementalMesh(solid, DEFLECTION_MM, False, ANGLE_RAD, True)
    out = []
    exp = TopExp_Explorer(solid, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        if tri is not None:
            trsf = loc.Transformation()
            v = np.array([tuple(tri.Node(i).Transformed(trsf).Coord()) for i in range(1, tri.NbNodes() + 1)])
            t = np.array([tri.Triangle(i).Get() for i in range(1, tri.NbTriangles() + 1)]) - 1
            if face.Orientation() == TopAbs_REVERSED:
                t = t[:, [0, 2, 1]]
            out.append((v, t))
        exp.Next()
    return out


# ------------------------------------------------------------------ classifying
def chip_size(ext_xz):
    long_, short = max(ext_xz), min(ext_xz)
    for L, W in CHIP_SIZES:
        if abs(long_ - L) < 0.25 * L and abs(short - W) < 0.3 * W:
            return True
    return False


def chip_boxes(lo, hi, cap):
    """A chip resistor or capacitor as a body and two metal end caps (boxes), in the board frame (Y up)."""
    ext = hi - lo
    ax = 0 if ext[0] >= ext[2] else 2                     # the long axis in the board plane
    t = 0.2 * ext[ax]
    boxes = []
    body_lo, body_hi = lo.copy(), hi.copy()
    body_lo[ax] += t; body_hi[ax] -= t
    body_lo[1] += 0.005; body_hi[1] -= 0.005
    boxes.append(("ceramic" if cap else "resistor", body_lo, body_hi))
    for end in (0, 1):
        c_lo, c_hi = lo.copy() - 0.01, hi.copy() + 0.01
        c_lo[1], c_hi[1] = lo[1], hi[1] + 0.01
        if end == 0:
            c_hi[ax] = lo[ax] + t
        else:
            c_lo[ax] = hi[ax] - t
        boxes.append(("tin", c_lo, c_hi))
    return [(m, trimesh.creation.box(extents=h - l, transform=trimesh.transformations.translation_matrix((l + h) / 2)))
            for m, l, h in boxes]


def chip_faces_split(faces, lo, hi):
    """A chip with its pins in one solid: faces low down at its edge are pins (tin), the rest is the body."""
    ext = np.maximum(hi - lo, 1e-6)
    out = []
    for v, t in faces:
        c = v.mean(axis=0)
        r = max(abs(c[0] - (lo[0] + hi[0]) / 2) / (ext[0] / 2), abs(c[2] - (lo[2] + hi[2]) / 2) / (ext[2] / 2))
        h = (c[1] - lo[1]) / ext[1]
        out.append(("tin" if r > 0.78 and h < 0.45 else "plastic", v, t))
    return out


def rings(pcb_faces, y_bot, y_top):
    """Tinned annular rings around the mounting holes: vertical cylinder walls through the whole plate, 1-2.5 mm
    radius, covering at least a third of a circle (a hole wall often comes as two half cylinders; the board's rounded
    corners are quarter circles and are left out). A least-squares circle fit gives the centre."""
    found = {}
    for v, t in pcb_faces:
        if np.ptp(v[:, 1]) < 0.8 * (y_top - y_bot) or len(v) < 6:
            continue
        x, z = v[:, 0], v[:, 2]
        A = np.column_stack([2 * x, 2 * z, np.ones_like(x)])
        (cx, cz, k), *_ = np.linalg.lstsq(A, x * x + z * z, rcond=None)
        r = float(np.sqrt(max(k + cx * cx + cz * cz, 0)))
        if not 1.0 < r < 2.5 or np.abs(np.hypot(x - cx, z - cz) - r).max() > 0.05:
            continue
        bins = np.unique(np.floor((np.degrees(np.arctan2(z - cz, x - cx)) + 180) / 10))
        if len(bins) < 12:
            continue
        found[(round(cx, 1), round(cz, 1))] = (cx, cz, r)
    out = []
    for cx, cz, r in found.values():
        for y in (y_top + 0.012, y_bot - 0.012):
            ring = trimesh.creation.annulus(r_min=r, r_max=r + 1.1, height=0.02, sections=48)
            ring.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))
            ring.apply_translation([cx, y, cz])
            out.append(("ring", ring))
    return out


def board_frame(pcb_faces, other_faces):
    """Turn and offset so the plate's thin axis is +Y with the components on top, centred on the origin."""
    pv = np.vstack([v for v, _ in pcb_faces])
    k = int(np.argmin(np.ptp(pv, axis=0)))
    plate = float(np.median(pv[:, k]))
    ov = np.vstack([v for v, _ in other_faces]) if other_faces else pv
    sign = 1.0 if float(np.median(ov[:, k])) >= plate else -1.0
    axes = {0: (np.pi / 2, [0, 0, 1]), 1: (0.0, [1, 0, 0]), 2: (-np.pi / 2, [1, 0, 0])}
    angle, about = axes[k]
    turn = trimesh.transformations.rotation_matrix(angle, about)
    if sign < 0:
        turn = trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1]) @ turn
    return turn


def classify(parts):
    """Triangles per material, in mm, in the board frame (Y up)."""
    tess = [faces_of(p["solid"]) for p in parts]
    sizes = [np.ptp(np.vstack([v for v, _ in f]), axis=0) if f else np.zeros(3) for f in tess]
    pcb_i = int(np.argmax([np.sort(s)[1] * np.sort(s)[2] for s in sizes]))
    turn = board_frame(tess[pcb_i], [fv for i, f in enumerate(tess) if i != pcb_i for fv in f])
    R = turn[:3, :3]
    tess = [[(v @ R.T, t) for v, t in f] for f in tess]
    pv = np.vstack([v for v, _ in tess[pcb_i]])
    ys = np.round(pv[:, 1], 2)
    vals, counts = np.unique(ys, return_counts=True)
    y_top, y_bot = (lambda two: (max(two), min(two)))(vals[np.argsort(counts)[-2:]])   # the plate's two faces
    groups = defaultdict(list)                            # material -> list of (vertices, triangles)
    by_instance = defaultdict(list)
    for i, p in enumerate(parts):
        by_instance[p["instance"]].append(i)
    box_of = {}                                           # the outline of each component instance, all its solids
    for inst, members in by_instance.items():
        vs = [v for j in members for v, _ in tess[j]]
        if vs:
            allv = np.vstack(vs)
            box_of[inst] = (allv.min(axis=0), allv.max(axis=0))
    for i, (p, faces) in enumerate(zip(parts, tess)):
        if not faces:
            continue
        if i == pcb_i:                                    # the plate is mask; anything standing on it (SolidWorks
            for v, t in faces:                            # merged the connectors into the board) is a connector
                inside = (v[:, 1] >= y_bot - 0.05).all() and (v[:, 1] <= y_top + 0.05).all()
                groups["mask" if inside else "cream"].append((v, t))
            for m, mesh in rings(faces, y_bot, y_top):
                groups[m].append((mesh.vertices, mesh.faces))
            continue
        allv = np.vstack([v for v, _ in faces])
        lo, hi = allv.min(axis=0), allv.max(axis=0)
        ext = hi - lo
        name, col = p["name"].upper(), p["colour"]
        siblings = by_instance[p["instance"]]
        largest = max(siblings, key=lambda j: np.prod(sizes[j]))
        rule = next((m for (frag, c), m in NAME_COLOUR_RULES.items() if frag in name and c == col), None)
        if rule:
            groups[rule].extend(faces)
        elif any(frag in name for frag in CONNECTOR_NAMES):
            groups["cream" if np.prod(sizes[i]) >= 0.25 * np.prod(sizes[largest]) else "tin"].extend(faces)
        elif (name.startswith(("C_", "R_", "LED_")) or (not name and len(siblings) == 1)) \
                and chip_size((box_of[p["instance"]][1] - box_of[p["instance"]][0])[[0, 2]]):
            if i != largest:                              # KiCad's chips come as body + terminals: one rebuilt box
                continue
            blo, bhi = box_of[p["instance"]]
            bext = bhi - blo
            cap = name.startswith("C_") or (not name and bext[1] >= 0.6 * min(bext[0], bext[2]))
            for m, box in chip_boxes(blo, bhi, cap):
                groups["led" if name.startswith("LED") and m != "tin" else m].append((box.vertices, box.faces))
        elif i != largest:                                # small solids of a component: pins and terminals
            groups["tin"].extend(faces)
        else:
            for m, v, t in chip_faces_split(faces, lo, hi):
                groups[m].append((v, t))
    return groups, turn


# ------------------------------------------------------------------ writing the GLB
def material(name: str):
    hex_colour, metal, rough = MATERIALS[name]
    # glTF colours are linear: convert the sRGB hex, or the board renders pale
    srgb = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [round(255 * (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)) for c in srgb]
    return trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        name=name, baseColorFactor=rgb + [255], metallicFactor=metal, roughnessFactor=rough, doubleSided=True))


def compress(path: Path) -> str:
    """Meshopt compression with gltfpack (Node.js): the file shrinks to a fraction, the browser decodes it with
    three.js's MeshoptDecoder. Named nodes are kept (-kn). Without Node.js the file stays as trimesh wrote it,
    which the viewer reads as well."""
    exe = os.environ.get("GLTFPACK") or shutil.which("gltfpack")
    npx = shutil.which("npx")
    cmd = [exe] if exe else ([npx, "--yes", "gltfpack@1.3.0"] if npx else None)
    if not cmd:
        print(f"note: no gltfpack (Node.js); {path.name} left uncompressed")
        return "uncompressed"
    packed = path.with_name(path.stem + ".packed.glb")
    subprocess.run(cmd + ["-i", str(path), "-o", str(packed), "-cc", "-kn"], check=True, capture_output=True)
    packed.replace(path)
    return "meshopt"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step", type=Path, default=DEFAULT_STEP, help="the STEP file of the board")
    ap.add_argument("--out", type=Path, default=OUT, help="the folder to write body.glb and viewer.json to")
    args = ap.parse_args(argv)
    if not args.step.exists():
        sys.exit(f"build_model: {args.step} not found; pass --step PATH")
    parts = read_parts(args.step)
    groups, _ = classify(parts)
    meshes = {}
    for m, pieces in groups.items():
        verts, tris, base = [], [], 0
        for v, t in pieces:
            verts.append(v); tris.append(np.asarray(t) + base); base += len(v)
        meshes[m] = trimesh.Trimesh(np.vstack(verts) / 1000.0, np.vstack(tris), process=True)
    allv = np.vstack([m.vertices for m in meshes.values()])
    offset = -(allv.min(axis=0) + allv.max(axis=0)) / 2
    scene = trimesh.Scene()
    for m, mesh in sorted(meshes.items()):
        mesh.apply_translation(offset)
        mesh.visual = material(m)
        scene.add_geometry(mesh, node_name=m, geom_name=m)
    out = args.out
    if out.exists():
        for old in out.iterdir():
            old.unlink()
    out.mkdir(parents=True, exist_ok=True)
    scene.export(out / "body.glb")
    packing = compress(out / "body.glb")
    config = {
        "body": "body.glb", "jaws": [], "colors": {}, "default": {"body": None, "opening": 0.0},
        "camera": {"azimuth_deg": -35, "polar_deg": 55, "fill": 1.15},
    }
    (out / "viewer.json").write_text(json.dumps(config, indent=1) + "\n", encoding="utf-8")
    ext = np.ptp(allv, axis=0) * 1000
    print(f"wrote {out}: body.glb {(out / 'body.glb').stat().st_size // 1024} KB ({packing}); "
          + ", ".join(f"{k} {len(v.faces)}" for k, v in sorted(meshes.items()))
          + f"; {len(parts)} solids, {ext[0]:.0f} x {ext[1]:.0f} x {ext[2]:.0f} mm")
    return 0


if __name__ == "__main__":
    sys.exit(main())
