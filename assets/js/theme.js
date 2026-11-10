/* theme.js — guna semula pilihan mod terang/gelap sebelum halaman dilukis (elak kelipan).
   Dimuat dalam <head> tanpa defer. Diasingkan daripada HTML supaya Content-Security-Policy
   boleh melarang semua skrip sebaris. */
try{var t=localStorage.getItem("ir-theme");if(t)document.documentElement.setAttribute("data-theme",t)}catch(e){}
