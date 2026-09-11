/* =============================================================================
   site.js — kelakuan asas yang dikongsi semua halaman.
   Tiada dependensi. Setiap modul menyemak kewujudan elemen dahulu, jadi fail
   yang sama boleh dimuatkan di mana-mana halaman.
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- [1] Tema --------------------------------------------------------- */
  /* Pilihan disimpan; jika tiada, keutamaan sistem digunakan. Skrip pra-muat
     dalam <head> yang menetapkan atribut awal supaya tiada kelipan putih. */
  var STORE = "ir-theme";

  function currentTheme() {
    return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function setTheme(name, persist) {
    root.setAttribute("data-theme", name);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", name === "dark" ? "#12110d" : "#f4f1e8");
    var btn = document.querySelector("[data-theme-toggle]");
    if (btn) {
      btn.setAttribute("aria-pressed", String(name === "dark"));
      btn.setAttribute("aria-label", name === "dark" ? "Tukar ke mod terang" : "Tukar ke mod gelap");
    }
    if (persist) {
      try { localStorage.setItem(STORE, name); } catch (e) { /* mod peribadi */ }
    }
    document.dispatchEvent(new CustomEvent("themechange", { detail: { theme: name } }));
  }

  setTheme(currentTheme(), false);

  var toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    toggle.addEventListener("click", function () {
      setTheme(currentTheme() === "dark" ? "light" : "dark", true);
    });
  }

  /* --- [2] Navigasi mudah alih ----------------------------------------- */
  var navBtn = document.querySelector("[data-nav-toggle]");
  var nav = document.getElementById("nav");

  if (navBtn && nav) {
    var closeNav = function () {
      nav.removeAttribute("data-open");
      navBtn.setAttribute("aria-expanded", "false");
    };

    navBtn.addEventListener("click", function () {
      var open = nav.getAttribute("data-open") === "true";
      if (open) { closeNav(); }
      else {
        nav.setAttribute("data-open", "true");
        navBtn.setAttribute("aria-expanded", "true");
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.getAttribute("data-open") === "true") {
        closeNav();
        navBtn.focus();
      }
    });

    /* Bila skrin dilebarkan, panel tidak boleh tersekat dalam keadaan terbuka. */
    window.matchMedia("(min-width: 761px)").addEventListener("change", function (e) {
      if (e.matches) closeNav();
    });
  }

  /* --- [3] Penapis kategori -------------------------------------------- */
  /* Menggantikan onclick sebaris + global `event` yang digunakan sebelum ini.
     Kini: aria-pressed betul, kiraan per kategori, dan keadaan "tiada hasil". */
  var filterBar = document.querySelector("[data-filters]");
  var listRoot = document.querySelector("[data-filterable]");

  if (filterBar && listRoot) {
    var items = Array.prototype.slice.call(listRoot.querySelectorAll("[data-category]"));
    var chips = Array.prototype.slice.call(filterBar.querySelectorAll("[data-filter]"));
    var empty = document.querySelector("[data-empty]");

    chips.forEach(function (chip) {
      var key = chip.getAttribute("data-filter");
      var n = key === "all" ? items.length : items.filter(function (it) {
        return it.getAttribute("data-category") === key;
      }).length;
      var counter = chip.querySelector(".chip__count");
      if (counter) counter.textContent = n < 10 ? "0" + n : String(n);
      if (n === 0) { chip.disabled = true; chip.title = "Belum ada catatan dalam kategori ini"; }
    });

    var applyFilter = function (key) {
      var shown = 0;
      items.forEach(function (it) {
        var match = key === "all" || it.getAttribute("data-category") === key;
        it.hidden = !match;
        if (match) shown++;
      });
      chips.forEach(function (c) {
        c.setAttribute("aria-pressed", String(c.getAttribute("data-filter") === key));
      });
      if (empty) empty.hidden = shown !== 0;
      renumber();
    };

    /* Nombor indeks dikira semula supaya sentiasa 01, 02, 03… selepas ditapis. */
    var renumber = function () {
      var n = 0;
      items.forEach(function (it) {
        if (it.hidden) return;
        n++;
        var target = it.querySelector("[data-num]");
        if (target) target.textContent = (n < 10 ? "0" : "") + n;
      });
    };

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        applyFilter(chip.getAttribute("data-filter"));
      });
    });

    renumber();
  }

  /* --- [4] Pendedahan semasa skrol ------------------------------------- */
  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (reveals.length) {
    if (reduced || !("IntersectionObserver" in window)) {
      reveals.forEach(function (el) { el.classList.add("is-in"); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
      reveals.forEach(function (el) { io.observe(el); });
    }
  }

  /* --- [5] Kemajuan bacaan --------------------------------------------- */
  var bar = document.querySelector("[data-progress]");
  var article = document.querySelector("[data-article]");

  if (bar && article) {
    var ticking = false;

    var update = function () {
      ticking = false;
      var rect = article.getBoundingClientRect();
      var total = rect.height - window.innerHeight;
      var done = total > 0 ? (-rect.top) / total : 0;
      done = done < 0 ? 0 : done > 1 ? 1 : done;
      bar.style.transform = "scaleX(" + done + ")";
      bar.setAttribute("aria-valuenow", String(Math.round(done * 100)));
    };

    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
  }

  /* --- [6] Tahun semasa dalam kaki halaman ----------------------------- */
  var yearSlots = document.querySelectorAll("[data-year]");
  if (yearSlots.length) {
    var y = String(new Date().getFullYear());
    Array.prototype.forEach.call(yearSlots, function (el) { el.textContent = y; });
  }

  /* --- [7] Kongsi ------------------------------------------------------ */
  var shareBtn = document.querySelector("[data-share]");
  if (shareBtn) {
    if (navigator.share) {
      shareBtn.hidden = false;
      shareBtn.addEventListener("click", function (e) {
        e.preventDefault();
        navigator.share({
          title: document.title,
          url: location.href
        }).catch(function () { /* pengguna membatalkan */ });
      });
    } else if (navigator.clipboard) {
      shareBtn.hidden = false;
      shareBtn.addEventListener("click", function (e) {
        e.preventDefault();
        navigator.clipboard.writeText(location.href).then(function () {
          var label = shareBtn.querySelector("[data-share-label]");
          if (!label) return;
          var was = label.textContent;
          label.textContent = "Pautan disalin";
          setTimeout(function () { label.textContent = was; }, 2000);
        });
      });
    }
  }
})();
