#!/usr/bin/env python3
"""Build the 3D model the landing page's viewer shows, from the driver's STEP file.

    python tools/build_model.py --step PATH

Writes docs/assets/models/spectral/: body.glb (the board as two meshes, the PCB and everything mounted on it,
tessellated from the STEP and decimated for the web) and viewer.json for docs/javascripts/gripper-viewer.js
(no jaws, no colour choice: the board is shown as it is). The board is turned so that its components point up
(glTF is Y-up) and centred. Needs cadquery's OCP (the Open CASCADE kernel), trimesh with fast-simplification and
numpy: the workspace's .venv-cad environment, not the docs one. The STEP file lives in the product repository
(STEP files/Spectral_micro_STEP.STEP); it is not copied into this one.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import trimesh
from OCP.BRep import BRep_Tool
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "models" / "spectral"
DEFAULT_STEP = ROOT.parent.parent / "projects" / "Spectral-Micro-BLDC-controller" / "STEP files" / "Spectral_micro_STEP.STEP"
DEFLECTION_MM = 0.05       # tessellation: the largest gap between the mesh and the true surface
MAX_FACES = {"pcb": 6000, "parts": 30000}
COLOURS = {"pcb": "#15181c", "parts": "#9aa0a6"}
PCB_MAX_THICKNESS_MM = 2.5


def read_step(path: Path):
    reader = STEPControl_Reader()
    if reader.ReadFile(str(path)) != IFSelect_RetDone:
        sys.exit(f"build_model: cannot read {path}")
    reader.TransferRoots()
    return reader.OneShape()


def solid_meshes(shape) -> list[trimesh.Trimesh]:
    """One mesh per solid of the shape, in metres."""
    BRepMesh_IncrementalMesh(shape, DEFLECTION_MM, False, 0.3, True)
    meshes = []
    exp = TopExp_Explorer(shape, TopAbs_SOLID)
    while exp.More():
        verts, faces = [], []
        fexp = TopExp_Explorer(exp.Current(), TopAbs_FACE)
        while fexp.More():
            face = TopoDS.Face_s(fexp.Current())
            loc = TopLoc_Location()
            tri = BRep_Tool.Triangulation_s(face, loc)
            if tri is not None:
                trsf = loc.Transformation()
                base = len(verts)
                for i in range(1, tri.NbNodes() + 1):
                    p = tri.Node(i).Transformed(trsf)
                    verts.append((p.X(), p.Y(), p.Z()))
                reverse = face.Orientation() == TopAbs_REVERSED
                for i in range(1, tri.NbTriangles() + 1):
                    a, b, c = tri.Triangle(i).Get()
                    faces.append((base + a - 1, base + c - 1, base + b - 1) if reverse else (base + a - 1, base + b - 1, base + c - 1))
            fexp.Next()
        if faces:
            meshes.append(trimesh.Trimesh(np.array(verts) / 1000.0, np.array(faces), process=True))
        exp.Next()
    return meshes


def decimate(mesh: trimesh.Trimesh, limit: int) -> trimesh.Trimesh:
    return mesh.simplify_quadric_decimation(face_count=limit) if len(mesh.faces) > limit else mesh


def material(hex_colour: str):
    rgb = [int(hex_colour[i:i + 2], 16) for i in (1, 3, 5)]
    return trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=rgb + [255], metallicFactor=0.1, roughnessFactor=0.6, doubleSided=True))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step", type=Path, default=DEFAULT_STEP, help="the STEP file of the board")
    args = ap.parse_args(argv)
    if not args.step.exists():
        sys.exit(f"build_model: {args.step} not found; pass --step PATH")
    meshes = solid_meshes(read_step(args.step))
    # the PCB: the thin solid with the largest footprint; everything else is mounted on it
    def footprint(m):
        e = np.sort(m.extents)
        return e[1] * e[2] if e[0] * 1000 < PCB_MAX_THICKNESS_MM else 0.0
    pcb = max(meshes, key=footprint)
    parts = trimesh.util.concatenate([m for m in meshes if m is not pcb])
    # turn the board: its thin axis becomes +Y, with the components on top
    k = int(np.argmin(pcb.extents))
    up = np.zeros(3)
    up[k] = 1.0 if parts.centroid[k] >= pcb.centroid[k] else -1.0
    turn = trimesh.geometry.align_vectors(up, [0.0, 1.0, 0.0])
    for m in (pcb, parts):
        m.apply_transform(turn)
    centre = np.vstack([pcb.bounds, parts.bounds])
    offset = -(centre.min(axis=0) + centre.max(axis=0)) / 2
    scene = trimesh.Scene()
    sizes = {}
    for name, m in (("pcb", pcb), ("parts", parts)):
        before = len(m.faces)
        m = decimate(m, MAX_FACES[name])
        m.apply_translation(offset)
        m.visual = material(COLOURS[name])
        scene.add_geometry(m, node_name=name, geom_name=name)
        sizes[name] = (before, len(m.faces))
    if OUT.exists():
        for old in OUT.iterdir():
            old.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    scene.export(OUT / "body.glb")
    config = {
        "body": "body.glb", "jaws": [], "colors": {}, "default": {"body": None, "opening": 0.0},
        "camera": {"azimuth_deg": -35, "polar_deg": 55, "fill": 1.15},
    }
    (OUT / "viewer.json").write_text(json.dumps(config, indent=1) + "\n", encoding="utf-8")
    ext = np.ptp(np.vstack([pcb.bounds, parts.bounds]), axis=0) * 1000
    print(f"wrote {OUT.relative_to(ROOT)}: body.glb {(OUT / 'body.glb').stat().st_size // 1024} KB; "
          + ", ".join(f"{k} {a}->{b} faces" for k, (a, b) in sizes.items())
          + f"; {len(meshes)} solids, {ext[0]:.0f} x {ext[1]:.0f} x {ext[2]:.0f} mm")
    return 0


if __name__ == "__main__":
    sys.exit(main())
