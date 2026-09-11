/* =============================================================================
   facet.js — objek faset interaktif untuk hero.
   Canvas 2D tulen, tanpa dependensi. Menggantikan Three.js (~600KB) yang
   sebelum ini dimuat hanya untuk hiasan.

   Ciri: seret dengan tetikus/sentuh, momentum, putaran automatik, kawalan
   papan kekunci, warna diambil dari CSS custom property (ikut mod terang/gelap),
   rAF dihentikan bila keluar viewport, dan satu bingkai statik sahaja bila
   pengguna memilih "reduce motion".
   ========================================================================== */
(function () {
  "use strict";

  var host = document.querySelector("[data-facet]");
  if (!host) return;

  var canvas = document.createElement("canvas");
  var ctx = canvas.getContext("2d");
  if (!ctx) return;
  host.insertBefore(canvas, host.firstChild);

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Algebra matriks 3x3 (baris-major) --------------------------------- */
  function ident() { return [1, 0, 0, 0, 1, 0, 0, 0, 1]; }

  function mul(a, b) {
    var o = new Array(9);
    for (var r = 0; r < 3; r++) {
      for (var c = 0; c < 3; c++) {
        o[r * 3 + c] = a[r * 3] * b[c] + a[r * 3 + 1] * b[3 + c] + a[r * 3 + 2] * b[6 + c];
      }
    }
    return o;
  }

  function axisRot(x, y, z, ang) {
    var c = Math.cos(ang), s = Math.sin(ang), t = 1 - c;
    return [
      t * x * x + c,     t * x * y - s * z, t * x * z + s * y,
      t * x * y + s * z, t * y * y + c,     t * y * z - s * x,
      t * x * z - s * y, t * y * z + s * x, t * z * z + c
    ];
  }

  function apply(m, p) {
    return [
      m[0] * p[0] + m[1] * p[1] + m[2] * p[2],
      m[3] * p[0] + m[4] * p[1] + m[5] * p[2],
      m[6] * p[0] + m[7] * p[1] + m[8] * p[2]
    ];
  }

  /* --- Geometri: ikosahedron -------------------------------------------- */
  var PHI = (1 + Math.sqrt(5)) / 2;

  function icosahedron(radius) {
    var raw = [];
    [-1, 1].forEach(function (a) {
      [-PHI, PHI].forEach(function (b) {
        raw.push([0, a, b], [a, b, 0], [b, 0, a]);
      });
    });
    var len = Math.sqrt(1 + PHI * PHI);
    var verts = raw.map(function (v) {
      return [v[0] / len * radius, v[1] / len * radius, v[2] / len * radius];
    });

    /* Rusuk dicari melalui jarak terdekat — kukuh tanpa jadual tetap. */
    var min = Infinity, i, j, d;
    for (i = 0; i < verts.length; i++) {
      for (j = i + 1; j < verts.length; j++) {
        d = dist(verts[i], verts[j]);
        if (d < min) min = d;
      }
    }
    var edges = [];
    for (i = 0; i < verts.length; i++) {
      for (j = i + 1; j < verts.length; j++) {
        if (dist(verts[i], verts[j]) < min * 1.05) edges.push([i, j]);
      }
    }
    return { verts: verts, edges: edges };
  }

  function dist(a, b) {
    var x = a[0] - b[0], y = a[1] - b[1], z = a[2] - b[2];
    return Math.sqrt(x * x + y * y + z * z);
  }

  function cube(s) {
    var v = [], e = [];
    [-s, s].forEach(function (x) {
      [-s, s].forEach(function (y) {
        [-s, s].forEach(function (z) { v.push([x, y, z]); });
      });
    });
    for (var i = 0; i < 8; i++) {
      for (var j = i + 1; j < 8; j++) {
        if (Math.abs(dist(v[i], v[j]) - 2 * s) < 1e-6) e.push([i, j]);
      }
    }
    return { verts: v, edges: e };
  }

  function tetra(s) {
    var v = [[s, s, s], [s, -s, -s], [-s, s, -s], [-s, -s, s]];
    return { verts: v, edges: [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]] };
  }

  function ring(radius, segments, tilt, spin) {
    var pts = [];
    for (var i = 0; i < segments; i++) {
      var a = (i / segments) * Math.PI * 2;
      pts.push([Math.cos(a) * radius, 0, Math.sin(a) * radius]);
    }
    var m = mul(axisRot(0, 0, 1, spin), axisRot(1, 0, 0, tilt));
    return pts.map(function (p) { return apply(m, p); });
  }

  var shell = icosahedron(1);
  var core = icosahedron(0.62);

  var rings = [
    { pts: ring(1.42, 96, 1.15, -0.22), weight: 1 },
    { pts: ring(1.62, 96, -0.95, 0.42), weight: 0.72 },
    { pts: ring(1.82, 96, 0.5, -0.62), weight: 0.5 }
  ];

  var floaters = [
    { mesh: cube(0.1), at: [1.52, 0.62, 0.15], spin: axisRot(0.6, 0.8, 0, 0.011) },
    { mesh: tetra(0.12), at: [-1.44, -0.6, 0.28], spin: axisRot(0.2, 0.9, 0.3, -0.009) },
    { mesh: icosahedron(0.1), at: [0.86, -1.32, -0.18], spin: axisRot(0.9, 0.1, 0.4, 0.013) }
  ];
  floaters.forEach(function (f) { f.rot = ident(); });

  var dots = [[1.78, -0.36, 0.22], [-1.7, 0.32, -0.1], [0.18, 1.66, 0.14], [-0.56, -1.76, -0.2]];

  /* --- Warna daripada CSS ---------------------------------------------- */
  var palette = {};

  function readPalette() {
    var cs = getComputedStyle(document.documentElement);
    palette.ink = rgb(cs.getPropertyValue("--ink"));
    palette.faint = rgb(cs.getPropertyValue("--ink-faint"));
    palette.rule = rgb(cs.getPropertyValue("--rule-strong"));
    palette.clay = rgb(cs.getPropertyValue("--clay"));
    palette.claySoft = rgb(cs.getPropertyValue("--clay-soft"));
  }

  function rgb(hex) {
    hex = (hex || "").trim().replace("#", "");
    if (hex.length === 3) hex = hex.replace(/./g, "$&$&");
    var n = parseInt(hex, 16);
    if (isNaN(n)) return [20, 19, 16];
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }

  function rgba(c, a) {
    return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a.toFixed(3) + ")";
  }

  readPalette();
  document.addEventListener("themechange", function () { readPalette(); draw(); });

  /* --- Kamera & saiz ---------------------------------------------------- */
  var W = 0, H = 0, scale = 1, dpr = 1;
  var CAM_Z = 3.6, FOCAL = 2.6;

  function resize() {
    var rect = host.getBoundingClientRect();
    if (!rect.width) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = rect.width;
    H = rect.height || rect.width;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    scale = Math.min(W, H) / 3.85;
    draw();
  }

  function project(p) {
    var z = CAM_Z - p[2];
    if (z < 0.05) z = 0.05;
    var k = (FOCAL / z) * scale;
    return { x: W / 2 + p[0] * k, y: H / 2 - p[1] * k, d: p[2] };
  }

  /* --- Keadaan putaran -------------------------------------------------- */
  var rot = mul(axisRot(1, 0, 0, -0.32), axisRot(0, 1, 0, 0.55));
  var velX = 0, velY = 0;
  var dragging = false, lastX = 0, lastY = 0;
  var AUTO = 0.0034;
  var t = 0;

  function spin(ax, ay, az, ang) { rot = mul(axisRot(ax, ay, az, ang), rot); }

  /* --- Lukisan ---------------------------------------------------------- */
  function drawMesh(mesh, m, offset, colour, baseWidth, baseAlpha) {
    var pts = mesh.verts.map(function (v) {
      var p = apply(m, v);
      if (offset) { p = [p[0] + offset[0], p[1] + offset[1], p[2] + offset[2]]; }
      return project(p);
    });

    mesh.edges.forEach(function (e) {
      var a = pts[e[0]], b = pts[e[1]];
      /* Isyarat kedalaman: rusuk hadapan lebih gelap & tebal. */
      var depth = (a.d + b.d) / 2;
      var f = (depth + 1.1) / 2.2;
      f = f < 0 ? 0 : f > 1 ? 1 : f;
      ctx.strokeStyle = rgba(colour, baseAlpha * (0.22 + f * 0.78));
      ctx.lineWidth = baseWidth * (0.55 + f * 0.65);
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    });
    return pts;
  }

  function drawRing(pts, m, colour, weight) {
    var proj = pts.map(function (p) { return project(apply(m, p)); });
    /* Dilukis sebagai serpihan supaya kedalaman boleh dinyatakan per segmen. */
    for (var i = 0; i < proj.length; i++) {
      var a = proj[i], b = proj[(i + 1) % proj.length];
      var f = (((a.d + b.d) / 2) + 1.9) / 3.8;
      f = f < 0 ? 0 : f > 1 ? 1 : f;
      ctx.strokeStyle = rgba(colour, weight * (0.1 + f * 0.75));
      ctx.lineWidth = 0.7 + f * 0.85;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }
  }

  function draw() {
    if (!W) return;
    ctx.clearRect(0, 0, W, H);
    ctx.lineJoin = "round";
    ctx.lineCap = "round";

    var breathe = reduced ? 1 : 1 + Math.sin(t * 0.9) * 0.014;
    var m = rot.map(function (v) { return v * breathe; });

    /* Aura lembut — memberi rasa jisim tanpa imej raster. */
    var r = Math.min(W, H) * 0.42;
    var g = ctx.createRadialGradient(W / 2, H / 2, r * 0.1, W / 2, H / 2, r);
    g.addColorStop(0, rgba(palette.clay, 0.07));
    g.addColorStop(0.55, rgba(palette.rule, 0.05));
    g.addColorStop(1, rgba(palette.rule, 0));
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(W / 2, H / 2, r, 0, Math.PI * 2);
    ctx.fill();

    rings.forEach(function (rg) { drawRing(rg.pts, m, palette.rule, rg.weight); });

    drawMesh(core, m, null, palette.claySoft, 0.9, 0.55);
    drawMesh(shell, m, null, palette.ink, 1.5, 0.95);

    /* Bucu sebagai titik kecil — menegaskan "faset". */
    shell.verts.forEach(function (v) {
      var p = project(apply(m, v));
      var f = (p.d + 1.1) / 2.2;
      f = f < 0 ? 0 : f > 1 ? 1 : f;
      ctx.fillStyle = rgba(palette.clay, 0.28 + f * 0.72);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 1.3 + f * 1.9, 0, Math.PI * 2);
      ctx.fill();
    });

    floaters.forEach(function (f, i) {
      var bob = reduced ? 0 : Math.sin(t * (1.1 + i * 0.24)) * 0.09;
      var at = [f.at[0], f.at[1] + bob, f.at[2]];
      drawMesh(f.mesh, mul(m, f.rot), apply(m, at), palette.ink, 1.05, 0.62);
    });

    dots.forEach(function (d, i) {
      var p = project(apply(m, d));
      var f = (p.d + 1.9) / 3.8;
      f = f < 0 ? 0 : f > 1 ? 1 : f;
      var tw = reduced ? 1 : 1 + Math.sin(t * 1.6 + i * 1.7) * 0.3;
      ctx.fillStyle = rgba(palette.faint, (0.15 + f * 0.5));
      ctx.beginPath();
      ctx.arc(p.x, p.y, (1.1 + f * 1.7) * tw, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  /* --- Gelung animasi (dihentikan bila keluar viewport) ----------------- */
  var visible = true, raf = null;

  function frame() {
    raf = null;
    t += 0.016;

    floaters.forEach(function (f) { f.rot = mul(f.spin, f.rot); });

    if (!dragging) {
      if (Math.abs(velX) > 0.0002 || Math.abs(velY) > 0.0002) {
        spin(0, 1, 0, velX);
        spin(1, 0, 0, velY);
        velX *= 0.945;
        velY *= 0.945;
      } else if (!reduced) {
        spin(0.18, 1, 0.06, AUTO);
      }
    }
    draw();
    if (visible && !reduced) raf = requestAnimationFrame(frame);
  }

  function start() {
    if (raf === null && visible && !reduced) raf = requestAnimationFrame(frame);
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible) start(); else if (raf) { cancelAnimationFrame(raf); raf = null; }
    }, { threshold: 0.01 }).observe(host);
  }

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) { if (raf) { cancelAnimationFrame(raf); raf = null; } }
    else start();
  });

  /* --- Interaksi -------------------------------------------------------- */
  var SENS = 0.0072;

  function engaged() { host.dataset.engaged = "true"; }

  host.addEventListener("pointerdown", function (e) {
    dragging = true;
    velX = velY = 0;
    lastX = e.clientX;
    lastY = e.clientY;
    engaged();
    if (host.setPointerCapture && e.pointerId !== undefined) {
      try { host.setPointerCapture(e.pointerId); } catch (err) { /* diabaikan */ }
    }
    e.preventDefault();
  });

  host.addEventListener("pointermove", function (e) {
    if (!dragging) return;
    var dx = e.clientX - lastX, dy = e.clientY - lastY;
    lastX = e.clientX;
    lastY = e.clientY;
    velX = dx * SENS;
    velY = dy * SENS;
    spin(0, 1, 0, velX);
    spin(1, 0, 0, velY);
    if (reduced) draw();
  });

  function release() {
    if (!dragging) return;
    dragging = false;
    if (reduced) { velX = velY = 0; draw(); }
    else start();
  }
  host.addEventListener("pointerup", release);
  host.addEventListener("pointercancel", release);
  host.addEventListener("lostpointercapture", release);

  /* Papan kekunci — dulu objek ini mustahil digerakkan tanpa tetikus. */
  host.addEventListener("keydown", function (e) {
    var step = 0.14, handled = true;
    switch (e.key) {
      case "ArrowLeft":  spin(0, 1, 0, -step); break;
      case "ArrowRight": spin(0, 1, 0, step); break;
      case "ArrowUp":    spin(1, 0, 0, -step); break;
      case "ArrowDown":  spin(1, 0, 0, step); break;
      default: handled = false;
    }
    if (handled) {
      e.preventDefault();
      engaged();
      draw();
    }
  });

  /* --- Kitaran hayat ---------------------------------------------------- */
  if ("ResizeObserver" in window) {
    new ResizeObserver(resize).observe(host);
  } else {
    window.addEventListener("resize", resize);
  }

  resize();
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(resize); }
  start();
  if (reduced) draw();
})();
