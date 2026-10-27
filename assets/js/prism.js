/* prism.js — satu objek bersegi yang berputar di laman utama.
   "Satu perkara, beribu perspektif": objek yang sama, tetapi setiap sudut
   menampakkan segi, cahaya dan bentuk yang berbeza.
   Canvas 2D tulen, tiada dependensi. Seret (tetikus/jari) atau guna anak
   panah papan kekunci untuk putar. Berhenti bila tidak kelihatan. */
(function () {
  "use strict";
  var stage = document.querySelector("[data-prism]");
  if (!stage) return;
  var canvas = document.createElement("canvas");
  var ctx = canvas.getContext("2d");
  if (!ctx) return;
  stage.appendChild(canvas);

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Bentuk: ikosahedron (20 segi tiga) ----------------------------- */
  var t = (1 + Math.sqrt(5)) / 2;
  var V = [
    [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
    [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
    [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]
  ].map(function (v) {
    var l = Math.hypot(v[0], v[1], v[2]);
    return [v[0] / l, v[1] / l, v[2] / l];
  });
  var F = [
    [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
    [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
    [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
    [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
  ];

  /* --- Matriks putaran ------------------------------------------------- */
  function mul(a, b) {
    var o = [];
    for (var r = 0; r < 3; r++) for (var c = 0; c < 3; c++)
      o[r * 3 + c] = a[r * 3] * b[c] + a[r * 3 + 1] * b[3 + c] + a[r * 3 + 2] * b[6 + c];
    return o;
  }
  function rotY(a) { var c = Math.cos(a), s = Math.sin(a); return [c, 0, s, 0, 1, 0, -s, 0, c]; }
  function rotX(a) { var c = Math.cos(a), s = Math.sin(a); return [1, 0, 0, 0, c, -s, 0, s, c]; }
  function apply(m, v) {
    return [m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
            m[3] * v[0] + m[4] * v[1] + m[5] * v[2],
            m[6] * v[0] + m[7] * v[1] + m[8] * v[2]];
  }

  var M = mul(rotX(-0.45), rotY(0.6));
  var vx = 0.0045, vy = 0.0016;          /* halaju putaran (radian/bingkai) */
  var AUTO_X = 0.0045, AUTO_Y = 0.0016;

  /* --- Warna dari CSS (ikut mod terang/gelap) -------------------------- */
  var col = {};
  function hex(c) {
    c = c.trim();
    if (c[0] === "#") {
      if (c.length === 4) c = "#" + c[1] + c[1] + c[2] + c[2] + c[3] + c[3];
      return [parseInt(c.substr(1, 2), 16), parseInt(c.substr(3, 2), 16), parseInt(c.substr(5, 2), 16)];
    }
    var m = c.match(/\d+/g);
    return m ? [+m[0], +m[1], +m[2]] : [31, 107, 82];
  }
  function readColors() {
    var cs = getComputedStyle(document.documentElement);
    col.accent = hex(cs.getPropertyValue("--accent") || "#1f6b52");
    col.bg = hex(cs.getPropertyValue("--bg") || "#fbfaf7");
    col.ink = hex(cs.getPropertyValue("--ink") || "#1d1d1b");
    col.dark = (col.bg[0] + col.bg[1] + col.bg[2]) < 300;
  }
  function mix(a, b, k) {
    return "rgb(" + Math.round(a[0] + (b[0] - a[0]) * k) + "," +
      Math.round(a[1] + (b[1] - a[1]) * k) + "," + Math.round(a[2] + (b[2] - a[2]) * k) + ")";
  }

  /* --- Saiz kanvas ------------------------------------------------------ */
  var W = 0, H = 0, dpr = 1;
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = stage.clientWidth; H = stage.clientHeight;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    canvas.style.width = W + "px"; canvas.style.height = H + "px";
    draw();
  }

  /* --- Lukis ------------------------------------------------------------- */
  var LIGHT = (function () { var l = [-0.45, -0.7, 0.55], n = Math.hypot(l[0], l[1], l[2]); return [l[0] / n, l[1] / n, l[2] / n]; })();

  function draw() {
    if (!W) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    var R = Math.min(W, H) * 0.36, cx = W / 2, cy = H / 2 - H * 0.03, cam = 3.2;

    /* bayang di bawah objek */
    ctx.beginPath();
    ctx.ellipse(cx, cy + R * 1.18, R * 0.7, R * 0.11, 0, 0, Math.PI * 2);
    ctx.fillStyle = col.dark ? "rgba(0,0,0,.45)" : "rgba(29,29,27,.08)";
    ctx.fill();

    var P = V.map(function (v) {
      var p = apply(M, v), s = cam / (cam - p[2]);
      return { x: cx + p[0] * R * s, y: cy + p[1] * R * s, z: p[2], w: p };
    });

    var faces = [];
    for (var i = 0; i < F.length; i++) {
      var a = P[F[i][0]], b = P[F[i][1]], c = P[F[i][2]];
      /* normal dalam ruang 3D (selepas putaran) */
      var u = [b.w[0] - a.w[0], b.w[1] - a.w[1], b.w[2] - a.w[2]];
      var v = [c.w[0] - a.w[0], c.w[1] - a.w[1], c.w[2] - a.w[2]];
      var n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
      var nl = Math.hypot(n[0], n[1], n[2]); n = [n[0] / nl, n[1] / nl, n[2] / nl];
      var cen = [(a.w[0] + b.w[0] + c.w[0]) / 3, (a.w[1] + b.w[1] + c.w[1]) / 3, (a.w[2] + b.w[2] + c.w[2]) / 3];
      if (n[0] * cen[0] + n[1] * cen[1] + n[2] * cen[2] < 0) n = [-n[0], -n[1], -n[2]];
      if (n[2] <= 0.02) continue;                 /* segi membelakangi kita */
      var lit = Math.max(0, n[0] * LIGHT[0] + n[1] * LIGHT[1] + n[2] * LIGHT[2]);
      faces.push({ a: a, b: b, c: c, z: cen[2], lit: lit });
    }
    faces.sort(function (p, q) { return p.z - q.z; });

    var light = col.dark ? col.ink : [255, 255, 255];
    var deep = col.dark ? col.bg : col.ink;
    faces.forEach(function (f) {
      ctx.beginPath();
      ctx.moveTo(f.a.x, f.a.y); ctx.lineTo(f.b.x, f.b.y); ctx.lineTo(f.c.x, f.c.y); ctx.closePath();
      /* segi gelap → aksen tua; segi terang → aksen cerah */
      var k = f.lit;
      var fill = k > 0.5
        ? mix(col.accent, light, (k - 0.5) * 1.1)
        : mix(deep, col.accent, 0.45 + k * 1.1);
      ctx.fillStyle = fill;
      ctx.fill();
      ctx.lineJoin = "round";
      ctx.lineWidth = 1;
      ctx.strokeStyle = col.dark ? "rgba(255,255,255,.18)" : "rgba(255,255,255,.55)";
      ctx.stroke();
    });
  }

  /* --- Gerakan & interaksi ---------------------------------------------- */
  var dragging = false, lx = 0, ly = 0, visible = true, raf = 0, last = 0;

  function step(ts) {
    raf = 0;
    if (!visible) return;
    var dt = last ? Math.min((ts - last) / 16.67, 3) : 1; last = ts;
    if (!dragging) {
      vx += (AUTO_X - vx) * 0.02 * dt;            /* kembali perlahan ke putaran asal */
      vy += (AUTO_Y - vy) * 0.02 * dt;
    }
    M = mul(mul(rotY(vx * dt), rotX(-vy * dt)), M);
    draw();
    if (!reduced) raf = requestAnimationFrame(step);
  }
  function kick() { if (!raf && !reduced && visible) { last = 0; raf = requestAnimationFrame(step); } }

  stage.addEventListener("pointerdown", function (e) {
    dragging = true; lx = e.clientX; ly = e.clientY;
    stage.setPointerCapture(e.pointerId);
    stage.classList.add("is-dragging");
  });
  stage.addEventListener("pointermove", function (e) {
    if (!dragging) return;
    var dx = e.clientX - lx, dy = e.clientY - ly; lx = e.clientX; ly = e.clientY;
    vx = dx * 0.008; vy = -dy * 0.008;
    M = mul(mul(rotY(vx), rotX(-vy)), M);
    draw();
    if (reduced) return;
  });
  function end() { dragging = false; stage.classList.remove("is-dragging"); kick(); }
  stage.addEventListener("pointerup", end);
  stage.addEventListener("pointercancel", end);

  stage.addEventListener("keydown", function (e) {
    var k = { ArrowLeft: [-0.25, 0], ArrowRight: [0.25, 0], ArrowUp: [0, 0.25], ArrowDown: [0, -0.25] }[e.key];
    if (!k) return;
    e.preventDefault();
    M = mul(mul(rotY(k[0]), rotX(-k[1])), M);
    draw();
  });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (en) {
      visible = en[0].isIntersecting;
      if (visible) kick();
    }).observe(stage);
  }
  document.addEventListener("visibilitychange", function () {
    visible = !document.hidden; if (visible) kick();
  });

  /* Tukar warna bila tema bertukar */
  new MutationObserver(function () { readColors(); draw(); })
    .observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () { readColors(); draw(); });

  readColors();
  resize();
  window.addEventListener("resize", resize);
  kick();
})();
