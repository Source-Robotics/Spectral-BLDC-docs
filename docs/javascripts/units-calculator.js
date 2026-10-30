/* The units calculator on Control modes: encoder ticks as turns, degrees and rpm, the practical speed limit
   from the pole pairs, and the torque from Kt and the current. The constants come from the element's data
   attributes. */
(function () {
  function setup() {
    document.querySelectorAll(".calc[data-ticks-per-rev]").forEach(function (el) {
      if (el.dataset.ready) return;
      el.dataset.ready = "1";
      var perRev = parseFloat(el.dataset.ticksPerRev), fe = parseFloat(el.dataset.maxElectricalHz);
      var q = function (n) { return el.querySelector("[name=" + n + "]"); };
      var out = function (n, v) { var o = el.querySelector("[data-out=" + n + "]"); if (o) o.textContent = v; };
      var ticks = q("ticks"), pp = q("pp"), kt = q("kt"), ma = q("ma");
      function update() {
        var turns = parseFloat(ticks.value || 0) / perRev;
        out("turns", turns.toFixed(3));
        out("deg", (turns * 360).toFixed(1) + "\u00b0");
        out("rpm", (turns * 60).toFixed(turns * 60 < 10 ? 1 : 0));
        out("ppout", pp.value);
        out("maxrpm", (fe / parseFloat(pp.value) * 60).toFixed(0));
        var nm = parseFloat(kt.value || 0) * parseFloat(ma.value || 0) / 1000;
        out("nm", nm.toFixed(nm < 0.1 ? 3 : 2) + " Nm");
        out("ncm", (nm * 100).toFixed(nm * 100 < 10 ? 1 : 0) + " N\u00b7cm");
      }
      [ticks, pp, kt, ma].forEach(function (x) { x.addEventListener("input", update); x.addEventListener("change", update); });
      update();
    });
  }
  if (window.document$ && window.document$.subscribe) { window.document$.subscribe(setup); }
  else if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", setup); }
  else { setup(); }
})();
