/* site.js — tema terang/gelap dan tahun semasa. Tiada dependensi. */
(function () {
  "use strict";
  var root = document.documentElement;
  var KEY = "ir-theme";

  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function apply(dark, save) {
    root.setAttribute("data-theme", dark ? "dark" : "light");
    var btn = document.querySelector("[data-theme-toggle]");
    if (btn) {
      btn.setAttribute("aria-pressed", String(dark));
      btn.setAttribute("aria-label", dark ? "Tukar ke mod terang" : "Tukar ke mod gelap");
    }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", dark ? "#141412" : "#fbfaf7");
    if (save) { try { localStorage.setItem(KEY, dark ? "dark" : "light"); } catch (e) {} }
  }

  apply(isDark(), false);

  var btn = document.querySelector("[data-theme-toggle]");
  if (btn) btn.addEventListener("click", function () { apply(!isDark(), true); });

  var y = String(new Date().getFullYear());
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = y; });
})();
