"""Jana semua halaman HTML ibrahimroslan.com dengan kepala & kaki yang seragam.

Cara guna (dari folder repo):  python3 _build/build.py
Perlu: pip install markdown
Folder _build tidak dimuat naik ke laman (lihat .vercelignore).
"""
import json, sys, pathlib

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.ibrahimroslan.com"
NAME = "Ibrahim Roslan"
EMAIL = "hello@ibrahimroslan.com"
OG = f"{SITE}/assets/img/og-ibrahim-roslan.png"
PHOTO = "/assets/img/ibrahim-roslan.jpg?v=3"
UPDATED = "2026-10-27"

PERSON = {
    "@type": "Person",
    "@id": f"{SITE}/#person",
    "name": NAME,
    "givenName": "Ibrahim",
    "familyName": "Roslan",
    "url": f"{SITE}/",
    "image": f"{SITE}{PHOTO}",
    "email": f"mailto:{EMAIL}",
    "description": "Penulis jurnal peribadi tentang buku, barang rumah dan keputusan besar hidup. Berasal dari Batu Gajah, Perak; kini di Putrajaya.",
    "birthPlace": {"@type": "Place", "name": "Batu Gajah, Perak, Malaysia"},
    "homeLocation": {"@type": "Place", "name": "Putrajaya, Malaysia"},
    "knowsLanguage": ["ms", "en"],
    # Tambah pautan profil awam anda di sini (LinkedIn, Instagram, X, Threads...).
    # Ini bantu Google faham bahawa semua profil itu milik orang yang sama.
    "sameAs": [],
}
if not PERSON['sameAs']:
    del PERSON['sameAs']
WEBSITE = {
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "url": f"{SITE}/",
    "name": NAME,
    "inLanguage": "ms-MY",
    "publisher": {"@id": f"{SITE}/#person"},
}

LOGO = ('<svg class="brand__logo" viewBox="0 0 64 64" aria-hidden="true">'
        '<rect width="64" height="64" rx="16" fill="#1f6b52"/>'
        '<path d="M43 0h5a16 16 0 0 1 16 16v5z" fill="#7cc7a6"/>'
        '<g fill="none" stroke="#fff" stroke-width="6.5" stroke-linecap="square">'
        '<path d="M18 19v27"/><path d="M29.5 46V19h8a8.25 8.25 0 0 1 0 16.5h-8"/><path d="M38 36.5l8 9.5"/></g></svg>')

SUN = ('<svg class="icon-sun" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true">'
       '<circle cx="8" cy="8" r="3.1"/><path d="M8 1v1.6M8 13.4V15M1 8h1.6M13.4 8H15M3.1 3.1l1.1 1.1M11.8 11.8l1.1 1.1M12.9 3.1l-1.1 1.1M4.2 11.8l-1.1 1.1"/></svg>')
MOON = ('<svg class="icon-moon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M13.2 9.6A5.6 5.6 0 0 1 6.4 2.8a5.6 5.6 0 1 0 6.8 6.8z"/></svg>')

NAV = [("/blog.html", "Blog"), ("/thought.html", "Thought"), ("/about.html", "Tentang")]


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def page(path, title, desc, body, *, og_type="website", graph=None, robots=None, active=None, prefix="", js=None, og=None):
    og_img = og or OG
    extra_js = ('\n<script src="' + js + '" defer></script>') if js else ""
    url = SITE + ("/" if path == "index.html" else "/" + path)
    graph = graph or [WEBSITE, {"@id": f"{SITE}/#person"}]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    nav = "\n".join(
        f'        <a href="{h}"{" aria-current=\"page\"" if active == h else ""}>{t}</a>' for h, t in NAV)
    robots_tag = f'<meta name="robots" content="{robots}">\n' if robots else ""
    return f"""<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots_tag}<link rel="canonical" href="{url}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#fbfaf7">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="ms_MY">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME} — satu perkara, beribu perspektif.">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{NAME} — Blog" href="/feed.xml">
<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/main.css?v=3">
<script>try{{var t=localStorage.getItem("ir-theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>

<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#utama">Langkau ke kandungan</a>

<header class="site-head">
  <div class="wrap site-head__inner">
    <a class="brand" href="/" aria-label="{NAME} — laman utama">
      {LOGO}
      <span class="brand__name">{NAME}</span>
    </a>
    <div class="site-head__right">
      <nav class="nav" aria-label="Navigasi utama">
{nav}
      </nav>
      <button class="theme-toggle" type="button" data-theme-toggle aria-pressed="false" aria-label="Tukar ke mod gelap">
        {SUN}{MOON}
      </button>
    </div>
  </div>
</header>

<main id="utama" class="wrap">
{body}
</main>

<footer class="site-foot">
  <div class="wrap">
    <ul class="site-foot__links">
      <li><a href="/blog.html">Blog</a></li>
      <li><a href="/thought.html">Thought</a></li>
      <li><a href="/about.html">Tentang saya</a></li>
      <li><a href="mailto:{EMAIL}">E-mel</a></li>
      <li><a href="/privacy.html">Dasar privasi</a></li>
      <li><a href="/disclaimer.html">Penafian</a></li>
      <li><a href="/feed.xml">RSS</a></li>
    </ul>
    <p>&copy; <span data-year>2026</span> {NAME} · Batu Gajah &rarr; Putrajaya</p>
  </div>
</footer>

<script src="/assets/js/site.js" defer></script>{extra_js}
</body>
</html>
"""


QUOTES = [
    ("Kita tidak jatuh ke tahap matlamat kita, tetapi kita jatuh ke tahap sistem kita.",
     "James Clear", "Atomic Habits",
     "Ayat inilah yang menukar cara saya fikir tentang azam. Matlamat cuma menetapkan arah; yang "
     "benar-benar menentukan kemajuan ialah rutin harian yang cukup kecil sampai tak perlu semangat untuk mula. "
     '<a href="/blog/review-buku-atomic-habits-bm.html">Baca pandangan penuh saya</a>.'),
    ("Adakah kita benar-benar inginkan perkara ini, atau kita cuma inginkan persepsi orang lain terhadap kita apabila kita memilikinya?",
     "Morgan Housel", "The Psychology of Money",
     "Soalan yang menyakitkan bila ditanya betul-betul, terutama sebelum membuat pembelian besar. Saya "
     "simpan ia sebagai penapis sebelum keputusan yang membawa komitmen kewangan panjang."),
]


def quotes(with_notes):
    items = []
    for q, who, book, note in QUOTES:
        n = f'\n      <p class="quote__note">{note}</p>' if with_notes else ""
        items.append(f"""    <li>
      <figure class="quote">
        <blockquote>{q}</blockquote>
        <figcaption class="quote__source">— {who}, <cite>{book}</cite></figcaption>{n}
      </figure>
    </li>""")
    return '  <ul class="quotes">\n' + "\n".join(items) + "\n  </ul>"



# ------------------------------------------------------------------ SENARAI ARTIKEL
# Artikel baharu: tambah di ATAS senarai ini (paling baru dahulu).
POSTS = [
    ("/blog/the-anxious-generation-kecewakan-anak.html",
     "The Anxious Generation: betul ke kita patut sengaja kecewakan anak? Pandangan peribadi saya",
     "Satu petikan tular kata ibu bapa patut kecewakan anak setiap hari. Saya selidik dari mana ia datang dan apa isi sebenar buku ni.",
     "2026-10-27", "27 Okt 2026", "Buku"),
    ("/blog/review-buku-atomic-habits-bm.html",
     "Atomic Habits versi BM: berbaloi beli atau tanya AI je? Pandangan peribadi saya",
     "Saya baca versi English tapi banyak belajar daripada perkongsian versi BM di media sosial.",
     "2026-09-08", "8 Sep 2026", "Buku"),
]

def posts_list(limit=None):
    rows = []
    for href, t, ex, iso, d, cat in POSTS[:limit]:
        rows.append(f"""    <li class="post">
      <a href="{href}">
        <span class="post__title">{t}</span>
        <span class="post__excerpt">{ex}</span>
        <span class="post__meta"><time datetime="{iso}">{d}</time> · {cat}</span>
      </a>
    </li>""")
    return '  <ul class="posts">\n' + "\n".join(rows) + "\n  </ul>"

# ====================================================================== ARTIKEL DARIPADA FAIL .md
# Artikel baharu: letak fail .md (format skill artikel-blog-ibrahimroslan) dalam _build/content/
# dan tambah satu baris dalam MD_ARTICLES di bawah. Kemudian jalankan:  python3 _build/build.py
import re as _re, html as _html
try:
    import markdown as _md
except ImportError:
    _md = None

CONTENT = pathlib.Path(__file__).resolve().parent / "content"
MONTHS = ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogo", "Sep", "Okt", "Nov", "Dis"]

# (nama fail tanpa .md, tarikh terbit YYYY-MM-DD, {nama produk: pautan affiliate})
MD_ARTICLES = [
    ("5-hukum-kebodohan-carlo-cipolla", "2026-10-28", {}),
]


def _meta(block, key):
    m = _re.search(r"^" + _re.escape(key) + r"[^:]*:\s*(.+)$", block, _re.M)
    return m.group(1).strip() if m else ""


def _ext_links(h):
    def fix(m):
        tag = m.group(0)
        if "rel=" in tag:
            return tag
        return tag[:-1] + ' target="_blank" rel="noopener">'
    return _re.sub(r'<a href="https?://[^"]+">', fix, h)


def md_article(slug, iso, affiliates):
    src = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    meta = ""
    m = _re.match(r"\s*<!--(.*?)-->", src, _re.S)
    if m:
        meta, src = m.group(1), src[m.end():]
    title = _re.search(r"^#\s+(.+)$", src, _re.M).group(1).strip()
    src = _re.sub(r"^#\s+.+$\n?", "", src, count=1, flags=_re.M).strip()
    lede, src = src.split("\n\n", 1)
    desc = _meta(meta, "Meta description") or lede
    cat = (_meta(meta, "Kategori") or "Blog").split("/")[0].strip()
    mins = _meta(meta, "Anggaran masa baca") or "5 minit"
    y, mo, d = iso.split("-")
    disp = f"{int(d)} {MONTHS[int(mo) - 1]} {y}"

    for name, link in affiliates.items():
        src = src.replace(f"[PAUTAN AFFILIATE: {name}]", link)
    body = _md.markdown(src, extensions=["extra", "sane_lists"])
    # Kotak "Jawapan ringkas"
    body = _re.sub(r"<blockquote>\s*<p><strong>Jawapan ringkas:?</strong>:?(.*?)</p>\s*</blockquote>",
                   r'<div class="note" style="margin-bottom:1.75rem"><p><strong>Jawapan ringkas:</strong>\1</p></div>',
                   body, flags=_re.S)
    # Pautan affiliate ditanda sponsored
    for link in affiliates.values():
        body = body.replace(f'<a href="{link}">', f'<a href="{link}" rel="sponsored nofollow noopener" target="_blank">')
    body = _ext_links(body)
    # Nota affiliate di hujung tidak perlu (kotak pendedahan di atas)
    body = _re.sub(r"<p><em>Catatan: Artikel ini mengandungi pautan affiliate.*?</p>", "", body, flags=_re.S)
    # Subtajuk ada id untuk pautan terus
    def _id(mh):
        t = _re.sub(r"<[^>]+>", "", mh.group(1))
        sid = _re.sub(r"[^a-z0-9]+", "-", _html.unescape(t).lower()).strip("-")[:60]
        return f'<h2 id="{sid}">{mh.group(1)}</h2>'
    body = _re.sub(r"<h2>(.*?)</h2>", _id, body)

    disclosure = ('<p class="disclosure">Artikel ini mengandungi pautan affiliate Shopee. Jika anda membeli melaluinya saya\n'
                  '      mungkin menerima komisen kecil tanpa kos tambahan kepada anda. <a href="/disclaimer.html">Baca penafian</a>.</p>\n'
                  if affiliates else "")
    short = title.split(":")[0].strip()
    url = f"{SITE}/blog/{slug}.html"
    plain_lede = _re.sub(r"<[^>]+>", "", _md.markdown(lede))
    page_body = f"""  <nav class="crumbs" aria-label="Laluan">
    <ol><li><a href="/">Laman utama</a></li><li><a href="/blog.html">Blog</a></li><li>{short}</li></ol>
  </nav>

  <article>
    <header class="page-head">
      <h1>{title}</h1>
      <p class="lead">{plain_lede.strip()}</p>
      <p class="article-meta">Oleh <a href="/about.html">{NAME}</a> · <time datetime="{iso}">{disp}</time> · {cat} · {mins} baca</p>
    </header>

    <div class="prose">
      {disclosure}{body}

      <div class="author">
        <img src="{PHOTO}" width="64" height="64" alt="{NAME}" loading="lazy">
        <p><strong>{NAME}</strong><br>Berkongsi pandangan peribadi tentang buku, media sosial dan keputusan hidup, dari Putrajaya.
        <a href="/about.html">Kenali saya</a>.</p>
      </div>
    </div>
  </article>"""
    graph = [WEBSITE, PERSON, {
        "@type": "BlogPosting", "@id": f"{url}#article", "headline": title, "description": desc,
        "datePublished": iso, "dateModified": iso, "url": url, "mainEntityOfPage": url,
        "inLanguage": "ms-MY", "image": OG,
        "author": {"@id": f"{SITE}/#person"}, "publisher": {"@id": f"{SITE}/#person"},
    }, {
        "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Laman utama", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog.html"},
            {"@type": "ListItem", "position": 3, "name": short, "item": url},
        ]}]
    post = (f"/blog/{slug}.html", title, plain_lede.strip(), iso, disp, cat)
    pg = (f"blog/{slug}.html", f"{title} | {NAME}", desc, page_body,
          dict(graph=graph, og_type="article", active="/blog.html"))
    return post, pg


MD_PAGES = []
if _md:
    for _slug, _iso, _aff in MD_ARTICLES:
        _post, _pg = md_article(_slug, _iso, _aff)
        POSTS.append(_post)
        MD_PAGES.append(_pg)
POSTS.sort(key=lambda p: p[3], reverse=True)

EMPTY_POSTS = """  <!-- SENARAI ARTIKEL
       Bila artikel pertama siap, padam kotak <div class="note"> di bawah dan guna format ini:
       <ul class="posts">
         <li class="post">
           <a href="/blog/nama-artikel.html">
             <span class="post__title">Tajuk artikel</span>
             <span class="post__excerpt">Ringkasan satu ayat.</span>
             <span class="post__meta"><time datetime="2026-11-01">1 Nov 2026</time> · Rumah</span>
           </a>
         </li>
       </ul>
  -->
  <div class="note">
    <p><strong>Artikel pertama sedang ditulis.</strong> Sementara itu, kenali
    <a href="/about.html">siapa saya dan apa yang akan saya tulis di sini</a>.</p>
  </div>"""

# ------------------------------------------------------------------ LAMAN UTAMA
home_body = f"""  <section class="hero hero--home" aria-labelledby="nama">
    <div class="hero__id">
      <div>
        <p class="hero__hello">Hai, saya</p>
        <h1 class="hero__name" id="nama">{NAME}</h1>
        <p class="hero__tagline">Satu perkara, beribu perspektif.</p>
      </div>
    </div>
    <figure class="prism">
      <div class="prism__stage" data-prism tabindex="0" role="img"
           aria-label="Satu objek bersegi yang berputar perlahan. Setiap sudut menampakkan rupa yang berbeza."></div>
      <figcaption>Satu objek. Setiap sudut, rupa berbeza.<span class="prism__hint"> Seret untuk putar.</span></figcaption>
    </figure>
  </section>

  <p class="lead">Saya berasal dari Batu Gajah, Perak dan kini menetap di Putrajaya. Di sini saya
  kongsi pandangan peribadi tentang buku dan perkongsian yang saya jumpa di media sosial, barang
  rumah yang saya beli dan keputusan besar seperti membina keluarga dan memiliki aset sendiri.</p>

  <div class="actions">
    <a class="btn" href="/about.html">Kenali saya</a>
    <a class="btn btn--ghost" href="/blog.html">Baca blog</a>
  </div>

  <section class="section" aria-labelledby="tajuk-terkini">
    <div class="section__head">
      <h2 class="section__title" id="tajuk-terkini">Penulisan terkini</h2>
      <a class="section__link" href="/blog.html">Semua blog &rarr;</a>
    </div>
{posts_list(3) if POSTS else EMPTY_POSTS}
  </section>

  <section class="section" aria-labelledby="tajuk-thought">
    <div class="section__head">
      <h2 class="section__title" id="tajuk-thought">Thought pilihan</h2>
      <a class="section__link" href="/thought.html">Semua thought &rarr;</a>
    </div>
{quotes(False)}
  </section>"""

home_graph = [WEBSITE, PERSON]

# ------------------------------------------------------------------ TENTANG
about_body = f"""  <section class="hero" aria-labelledby="nama">
    <img class="avatar" src="{PHOTO}" width="168" height="168" alt="Gambar {NAME}" fetchpriority="high">
    <div>
      <p class="hero__hello">Tentang saya</p>
      <h1 class="hero__name" id="nama">{NAME}</h1>
      <p class="hero__tagline">Batu Gajah &rarr; Putrajaya</p>
    </div>
  </section>

  <dl class="facts">
    <div><dt>Asal</dt><dd>Batu Gajah, Perak</dd></div>
    <div><dt>Kini</dt><dd>Putrajaya</dd></div>
    <div><dt>Bahasa</dt><dd>Melayu, Inggeris</dd></div>
    <div><dt>E-mel</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
  </dl>

  <div class="prose" style="padding-top:0">
    <p class="lead">Saya Ibrahim Roslan. Laman ini ruang perkongsian peribadi saya. Semua yang ada di
    sini datang daripada apa yang saya sendiri lalui, bukan teori.</p>

    <p>Saya bercerita tentang pengalaman hidup dan keputusan yang saya betul-betul buat, bermula
    daripada yang kecil seperti memilih perkakas rumah, sampai kepada keputusan besar yang membawa
    komitmen kewangan panjang, termasuklah membina keluarga dan merancang untuk memiliki aset sendiri.</p>

    <p>Apa yang saya kongsikan berdasarkan apa yang telah saya lalui setakat ini. Saya juga tidak lari
    daripada melakukan kesilapan dan kesilapan itu pun saya tulis.</p>

    <h2>Kenapa nama "Satu perkara, beribu perspektif"?</h2>
    <p>Apa yang kita lihat selalunya cuma satu sisi daripada keseluruhan cerita, termasuk apa yang
    saya tulis di sini. Saya kongsi sisi saya dan berharap dapat belajar daripada sisi
    orang lain juga.</p>

    <h2>Apa yang saya tulis</h2>
    <ul>
      <li><strong>Buku &amp; media sosial</strong>: pandangan peribadi tentang buku yang saya baca dan perkongsian yang saya jumpa di media sosial, serta pengajaran yang saya ambil daripadanya.</li>
      <li><strong>Perkakas &amp; barang rumah</strong>: apa yang saya beli, kenapa dan sama ada saya akan beli semula.</li>
      <li><strong>Keputusan besar</strong>: kewangan, keluarga dan aset, ditulis sebagai catatan perjalanan, bukan nasihat profesional.</li>
    </ul>

    <!-- PROFIL LAIN: bila ada, buang komen ini dan senaraikan pautan profil awam anda.
    <h2>Di mana lagi anda boleh jumpa saya</h2>
    <ul>
      <li><a href="https://www.linkedin.com/in/..." rel="me">LinkedIn</a></li>
      <li><a href="https://www.instagram.com/..." rel="me">Instagram</a></li>
    </ul>
    -->

    <h2>Berhubung</h2>
    <p>Ada soalan, nak betulkan saya, atau sekadar mahu menyapa? E-mel saya di
    <a href="mailto:{EMAIL}">{EMAIL}</a>. Saya baca semua, walaupun kadang lambat balas.</p>
  </div>"""

about_graph = [WEBSITE, PERSON, {
    "@type": "ProfilePage",
    "@id": f"{SITE}/about.html#page",
    "url": f"{SITE}/about.html",
    "name": f"Tentang {NAME}",
    "inLanguage": "ms-MY",
    "dateModified": UPDATED,
    "mainEntity": {"@id": f"{SITE}/#person"},
}]

# ------------------------------------------------------------------ BLOG
blog_body = f"""  <header class="page-head">
    <h1>Blog</h1>
    <p class="lead">Pandangan peribadi tentang buku dan media sosial, panduan memilih barang rumah dan pengalaman peribadi. Setiap satu
    ditulis selepas saya sendiri melaluinya.</p>
  </header>

  <section class="section" style="border-top:0" aria-label="Senarai artikel">
{posts_list() if POSTS else EMPTY_POSTS}
  </section>"""

# ------------------------------------------------------------------ THOUGHT
thought_body = f"""  <header class="page-head">
    <h1>Thought</h1>
    <p class="lead">Kata-kata dan persoalan yang melekat lama selepas saya membacanya. Disimpan di
    sini sebagai peringatan untuk diri sendiri, bukan sebagai nasihat.</p>
  </header>

  <section class="section" style="border-top:0" aria-label="Senarai thought">
{quotes(True)}
  </section>"""

# ------------------------------------------------------------------ PRIVASI
privacy_body = f"""  <nav class="crumbs" aria-label="Laluan"><ol><li><a href="/">Laman utama</a></li><li>Dasar privasi</li></ol></nav>
  <header class="page-head">
    <h1>Dasar privasi</h1>
    <p class="lead">Apa yang laman ini kumpul, apa yang tidak dan siapa lagi yang mungkin melihat kunjungan anda.</p>
    <p class="article-meta">Kemas kini: <time datetime="{UPDATED}">27 Okt 2026</time></p>
  </header>
  <div class="prose">
    <p>Privasi pelawat penting kepada saya. Halaman ini menerangkan maklumat yang dikumpul apabila anda
    melawat <strong>ibrahimroslan.com</strong>, dalam bahasa biasa, bukan bahasa peguam.</p>

    <h2>Maklumat yang dikumpul</h2>
    <p>Laman ini mungkin menggunakan perkhidmatan analisis trafik ringkas untuk melihat maklumat asas
    seperti jumlah paparan halaman, jenis pelayar dan jenis peranti. Maklumat ini bersifat agregat dan
    tidak mengenal pasti anda sebagai individu.</p>
    <p>Saya tidak mempunyai borang pendaftaran, tidak menyimpan senarai e-mel dan tidak meminta nama
    atau nombor telefon anda di mana-mana halaman.</p>

    <h2>Cookies dan pihak ketiga</h2>
    <p>Laman ini sendiri hanya menyimpan satu pilihan kecil dalam pelayar anda: sama ada anda memilih
    mod terang atau gelap. Pautan <em>affiliate</em> yang saya guna (contohnya Shopee) mungkin
    menggunakan cookies di laman mereka untuk mengesan rujukan. Butiran ada di halaman
    <a href="/disclaimer.html">Penafian</a>.</p>

    <h2>Pautan luar</h2>
    <p>Setelah anda klik keluar ke laman lain, dasar privasi laman tersebut yang terpakai. Saya tidak
    bertanggungjawab ke atas kandungan atau amalan privasi laman pihak ketiga.</p>

    <h2>Perubahan pada dasar ini</h2>
    <p>Jika dasar ini dikemas kini, tarikh di atas akan berubah dan perubahan besar akan dinyatakan dengan jelas.</p>

    <h2>Hubungi saya</h2>
    <p>Ada soalan tentang dasar ini? E-mel saya di <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>"""

# ------------------------------------------------------------------ PENAFIAN
disclaimer_body = f"""  <nav class="crumbs" aria-label="Laluan"><ol><li><a href="/">Laman utama</a></li><li>Penafian</li></ol></nav>
  <header class="page-head">
    <h1>Penafian</h1>
    <p class="lead">Dari mana kandungan ini datang, bila saya dapat komisen dan apa yang anda patut semak sendiri sebelum membeli.</p>
    <p class="article-meta">Kemas kini: <time datetime="{UPDATED}">27 Okt 2026</time></p>
  </header>
  <div class="prose">
    <h2>Kandungan ini pengalaman peribadi</h2>
    <p>Semua maklumat, pandangan dan cerita di <strong>ibrahimroslan.com</strong> berdasarkan
    pengalaman peribadi saya. Ia untuk maklumat umum, bukan nasihat profesional sama ada kewangan,
    undang-undang, perubatan atau teknikal.</p>
    <p>Apa yang sesuai untuk saya, dengan bajet dan keadaan saya, mungkin tidak sesuai untuk anda.
    Timbang sendiri sebelum ikut.</p>

    <h2>Pendedahan pautan affiliate</h2>
    <p>Sesetengah artikel mungkin mengandungi pautan <em>affiliate</em> ke platform seperti Shopee.
    Jika anda membeli melalui pautan tersebut, saya mungkin menerima komisen kecil,
    <strong>tanpa sebarang kos tambahan kepada anda</strong>.</p>
    <p>Peraturan yang saya pegang:</p>
    <ul>
      <li>Saya hanya pautkan barang yang saya sendiri guna, beli, atau kaji secara serius.</li>
      <li>Komisen tidak mengubah penilaian saya. Kalau sesuatu tak berbaloi, saya tulis ia tak berbaloi.</li>
      <li>Setiap artikel yang ada pautan affiliate akan menyatakannya di dalam artikel itu sendiri.</li>
    </ul>

    <h2>Ketepatan maklumat</h2>
    <p>Saya cuba pastikan maklumat tepat pada masa penulisan, tetapi harga, stok, spesifikasi dan
    dasar penjual boleh berubah. Sentiasa semak maklumat terkini di halaman produk sebelum membeli.</p>

    <h2>Tiada jaminan hasil</h2>
    <p>Bila saya tulis tentang tabiat atau keputusan hidup, saya bercerita tentang apa yang berlaku
    kepada saya. Tiada jaminan anda akan dapat hasil yang sama.</p>

    <h2>Soalan?</h2>
    <p>Kalau ada apa-apa yang tidak jelas atau tidak adil, beritahu saya di
    <a href="mailto:{EMAIL}">{EMAIL}</a>. Saya lebih rela betulkan daripada biarkan.</p>
  </div>"""

# ------------------------------------------------------------------ 404
nf_body = """  <header class="page-head" style="border-bottom:0">
    <h1>Halaman ini tak ada.</h1>
    <p class="lead">Halaman yang anda cari sudah dipindahkan atau memang tak pernah ada.</p>
    <div class="actions">
      <a class="btn" href="/">Laman utama</a>
      <a class="btn btn--ghost" href="/blog.html">Blog</a>
    </div>
  </header>"""

# ------------------------------------------------------------------ TEMPLAT ARTIKEL
tpl_body = f"""<!-- =====================================================================
     TEMPLAT ARTIKEL — cara guna:
     1. Salin fail ini ke /blog/nama-artikel.html (huruf kecil, guna tanda -).
     2. Ganti semua yang bertanda [ ... ] , termasuk dalam <head> di atas:
        <title>, description, canonical, og:title, og:description, og:url,
        dan blok JSON-LD (headline, datePublished, url).
     3. Buang baris <meta name="robots" content="noindex"> di atas.
     4. Tambah artikel ke senarai di blog.html dan index.html, serta
        sitemap.xml dan feed.xml.
     ===================================================================== -->
  <nav class="crumbs" aria-label="Laluan">
    <ol><li><a href="/">Laman utama</a></li><li><a href="/blog.html">Blog</a></li><li>[Tajuk ringkas]</li></ol>
  </nav>

  <article>
    <header class="page-head">
      <h1>[Tajuk artikel]</h1>
      <p class="lead">[Ringkasan satu atau dua ayat.]</p>
      <p class="article-meta">Oleh <a href="/about.html">{NAME}</a> · <time datetime="2026-11-01">[1 Nov 2026]</time> · [Kategori]</p>
    </header>

    <div class="prose">
      <!-- Kalau ada pautan affiliate, kekalkan kotak ini. Kalau tiada, padam. -->
      <p class="disclosure">Artikel ini mengandungi pautan affiliate. Jika anda membeli melaluinya, saya
      mungkin menerima komisen kecil tanpa kos tambahan kepada anda. <a href="/disclaimer.html">Baca penafian</a>.</p>

      <p>[Perenggan pembuka.]</p>

      <h2>[Subtajuk]</h2>
      <p>[Isi.]</p>

      <!-- Gambar sendiri: letak fail dalam /assets/img/ -->
      <figure>
        <img src="/assets/img/[nama-gambar].jpg" width="1200" height="800" alt="[Terangkan gambar]" loading="lazy">
        <figcaption>[Kapsyen gambar]</figcaption>
      </figure>

      <div class="buybox">
        <h3>Di mana saya beli</h3>
        <ul>
          <li><a href="[pautan]" rel="sponsored nofollow" target="_blank">[Nama kedai / produk]</a></li>
        </ul>
      </div>

      <div class="author">
        <img src="{PHOTO}" width="64" height="64" alt="{NAME}" loading="lazy">
        <p><strong>{NAME}</strong><br>Menulis tentang keputusan hidup yang betul-betul dilalui, dari Putrajaya.
        <a href="/about.html">Kenali saya</a>.</p>
      </div>
    </div>
  </article>"""

tpl_graph = [WEBSITE, PERSON, {
    "@type": "BlogPosting",
    "headline": "[Tajuk artikel]",
    "datePublished": "2026-11-01",
    "dateModified": "2026-11-01",
    "url": f"{SITE}/blog/[nama-artikel].html",
    "inLanguage": "ms-MY",
    "author": {"@id": f"{SITE}/#person"},
    "publisher": {"@id": f"{SITE}/#person"},
    "image": OG,
}]

# ------------------------------------------------------------------ ARTIKEL: ATOMIC HABITS
AH_URL = f"{SITE}/blog/review-buku-atomic-habits-bm.html"
AH_TITLE = "Atomic Habits versi BM: berbaloi beli atau tanya AI je? Pandangan peribadi saya"
AH_LEDE = "Saya baca versi English tapi banyak belajar daripada perkongsian versi Bahasa Melayu di media sosial. Ini pandangan peribadi saya, plus cara elak buku cetak rompak."
ah_body = f"""  <nav class="crumbs" aria-label="Laluan">
    <ol><li><a href="/">Laman utama</a></li><li><a href="/blog.html">Blog</a></li><li>Atomic Habits versi BM</li></ol>
  </nav>

  <article>
    <header class="page-head">
      <h1>{AH_TITLE}</h1>
      <p class="lead">{AH_LEDE}</p>
      <p class="article-meta">Oleh <a href="/about.html">{NAME}</a> · <time datetime="2026-09-08">8 Sep 2026</time>
      · Dikemas kini <time datetime="{UPDATED}">27 Okt 2026</time> · Buku · 5 minit baca</p>
    </header>

    <div class="prose">
      <p class="disclosure">Artikel ini mengandungi pautan affiliate Shopee. Jika anda membeli melaluinya saya
      mungkin menerima komisen kecil tanpa kos tambahan kepada anda. <a href="/disclaimer.html">Baca penafian</a>.</p>

      <div class="note" style="margin-bottom:1.75rem">
        <p><strong>Kandungan</strong></p>
        <ol style="margin:0.4rem 0 0">
          <li><a href="#versi-english-dan-bm">Saya baca versi English tapi belajar banyak dari versi BM</a></li>
          <li><a href="#4-undang-undang">Empat undang-undang perubahan tabiat</a></li>
          <li><a href="#kesan">Apa yang berubah selepas saya amalkan</a></li>
          <li><a href="#cetak-rompak">Awas buku cetak rompak</a></li>
          <li><a href="#keputusan">Berbaloi beli atau cukup tanya AI?</a></li>
        </ol>
      </div>

      <p>Buku <cite>Atomic Habits</cite> tulisan James Clear ni dah jadi macam kitab wajib untuk sesiapa
      yang nak ubah hidup. Bila terbit versi terjemahan Bahasa Melayu ramai yang tanya: <em>"Perlu ke
      beli atau suruh AI ringkaskan je?"</em></p>
      <p>Ini bukan ulasan buku yang lengkap. Ini pandangan peribadi saya tentang apa yang saya faham,
      apa yang saya cuba amalkan dan apa yang saya belajar daripada cerita orang lain.</p>

      <!-- GAMBAR: ambil gambar buku anda sendiri, simpan sebagai /assets/img/atomic-habits.jpg, kemudian buang komen ini.
      <figure>
        <img src="/assets/img/atomic-habits.jpg" width="1200" height="900" alt="Buku Atomic Habits milik Ibrahim Roslan" loading="lazy">
        <figcaption>Naskhah yang saya baca.</figcaption>
      </figure>
      -->

      <h2 id="versi-english-dan-bm">1. Saya baca versi English tapi belajar banyak dari versi BM</h2>
      <p>Saya baca <cite>Atomic Habits</cite> dalam versi asal bahasa Inggeris. Tapi selepas habis
      membaca saya perasan ramai orang berkongsi petikan dan pengalaman daripada versi Bahasa Melayu di
      media sosial.</p>
      <p>Membaca semula idea yang sama dalam bahasa kita memberi rasa yang berbeza. Ada ayat yang lebih
      mudah melekat bila dibaca dalam Bahasa Melayu. Yang lebih penting, perkongsian mereka tunjuk
      bagaimana orang biasa mengamalkan isi buku ini dalam hidup sebenar. Daripada cerita-cerita itulah
      saya banyak ambil pengajaran.</p>
      <p>Sebab itu saya rasa versi BM ni berbaloi wujud. Ia buat idea yang bagus lebih mudah sampai
      kepada lebih ramai orang.</p>

      <h2 id="4-undang-undang">2. Empat undang-undang perubahan tabiat</h2>
      <p>Intipati buku ni berkisar pada empat hukum utama untuk bina tabiat baik atau buang tabiat buruk:</p>
      <ul>
        <li><strong>Jadikannya nyata</strong> (<em>cue</em>): isyarat kena jelas depan mata.</li>
        <li><strong>Jadikannya menarik</strong> (<em>craving</em>): gabungkan tabiat yang nak dibina dengan perkara yang kita suka.</li>
        <li><strong>Jadikannya mudah</strong> (<em>response</em>): kurangkan halangan, contohnya peraturan 2 minit.</li>
        <li><strong>Jadikannya memuaskan</strong> (<em>reward</em>): wujudkan ganjaran segera.</li>
      </ul>

      <h2 id="kesan">3. Apa yang berubah selepas saya amalkan</h2>
      <p>Ayat yang paling melekat dalam kepala saya sampai sekarang datang daripada versi BM yang ramai kongsi:</p>
      <blockquote>Kita tidak jatuh ke tahap matlamat kita, tetapi kita jatuh ke tahap sistem kita.</blockquote>
      <p>Sebelum ni kalau nak buat sesuatu saya set matlamat besar. Bila penat semuanya terbengkalai.
      Lepas faham konsep sistem saya mula buat perubahan kecil yang konsisten. Contohnya saya kemas meja
      kerja setiap petang walaupun penat. Tak guna tenaga mental yang banyak pun.</p>
      <p>Perkara yang sama saya nampak dalam banyak perkongsian di media sosial. Perubahan kecil yang
      diulang setiap hari lebih mudah dikekalkan berbanding azam besar yang hanya bertahan seminggu.</p>

      <h2 id="cetak-rompak">4. Awas buku cetak rompak</h2>
      <p>Ini perkara yang saya perasan bila tengok buku ni dijual dalam talian. Ada penjual yang jual
      pada harga sekitar RM15 hingga RM20 sahaja. Pada harga serendah itu <strong>hampir pasti ia cetak
      rompak</strong>.</p>
      <p>Ramai juga yang berkongsi pengalaman beli naskhah begini: kualiti kertas teruk, bau gam kuat dan
      cetakan tulisan senget. Duit memang jimat sikit tapi rasa tak berkat. Pastikan beli naskhah asli
      walaupun harganya lebih tinggi.</p>

      <h2 id="keputusan">5. Berbaloi beli atau cukup tanya AI?</h2>
      <p>Kalau anda cuma nak tahu empat hukum di atas, ringkasan AI atau perkongsian di media sosial dah
      cukup dalam masa 5 minit. <strong>Tetapi</strong> buku ni bukan sekadar senarai hukum. Ia penuh
      dengan kisah dan contoh yang membentuk cara kita berfikir.</p>
      <p>Bagi saya <strong>ia berbaloi dibeli</strong> kalau anda serius nak ubah rutin hidup. Pilih
      versi English kalau selesa dengan bahasa Inggeris atau versi BM kalau nak bacaan yang lebih santai
      dan dekat dengan bahasa kita.</p>

      <div class="buybox">
        <h3>Di mana nak beli naskhah asli</h3>
        <ul>
          <li><a href="https://s.shopee.com.my/40gQrkgSLC" rel="sponsored nofollow noopener" target="_blank"><strong>Versi Bahasa Melayu</strong> di Shopee &rarr;</a></li>
          <li><a href="https://s.shopee.com.my/9056p03rZk" rel="sponsored nofollow noopener" target="_blank"><strong>Versi asal bahasa Inggeris</strong> (yang saya baca) di Shopee &rarr;</a></li>
        </ul>
        <p style="margin:0.75rem 0 0;font-size:var(--fs-small);color:var(--ink-faint)">Kedua-dua penjual ini menjual naskhah asli. Harga di Shopee boleh berubah jadi semak sebelum bayar.</p>
      </div>

      <p>Petikan ini saya simpan juga di halaman <a href="/thought.html">Thought</a>.</p>

      <div class="author">
        <img src="{PHOTO}" width="64" height="64" alt="{NAME}" loading="lazy">
        <p><strong>{NAME}</strong><br>Berkongsi pandangan peribadi tentang buku, media sosial dan keputusan hidup, dari Putrajaya.
        <a href="/about.html">Kenali saya</a>.</p>
      </div>
    </div>
  </article>"""

ah_graph = [WEBSITE, PERSON, {
    "@type": "BlogPosting",
    "@id": f"{AH_URL}#article",
    "headline": AH_TITLE,
    "description": "Pandangan peribadi tentang buku Atomic Habits: dibaca dalam English, banyak belajar daripada perkongsian versi Bahasa Melayu di media sosial, plus cara elak buku cetak rompak.",
    "datePublished": "2026-09-08",
    "dateModified": UPDATED,
    "url": AH_URL,
    "mainEntityOfPage": AH_URL,
    "inLanguage": "ms-MY",
    "image": f"{SITE}/assets/img/og-atomic-habits.png",
    "author": {"@id": f"{SITE}/#person"},
    "publisher": {"@id": f"{SITE}/#person"},
    "about": {"@type": "Book", "name": "Atomic Habits", "author": {"@type": "Person", "name": "James Clear"}},
}, {
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Laman utama", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog.html"},
        {"@type": "ListItem", "position": 3, "name": "Atomic Habits versi BM", "item": AH_URL},
    ],
}]

# ------------------------------------------------------------------ ARTIKEL: THE ANXIOUS GENERATION
AG_SLUG = "the-anxious-generation-kecewakan-anak"
AG_URL = f"{SITE}/blog/{AG_SLUG}.html"
AG_TITLE = "The Anxious Generation: betul ke kita patut sengaja kecewakan anak? Pandangan peribadi saya"
AG_LEDE = ("Satu petikan tular kata ibu bapa patut kecewakan anak setiap hari. Saya selidik dari mana ia datang, "
           "apa isi sebenar buku Jonathan Haidt ni dan bila rasa kecewa jadi baik atau memudaratkan.")
AG_DESC = ("Betul ke The Anxious Generation suruh kita kecewakan anak? Ringkasan buku Jonathan Haidt, "
           "cara ajar anak kawal emosi dan bila kecewa jadi memudaratkan.")
AG_SHOPEE = "https://s.shopee.com.my/BUuUvHXIE?share_channel_code=1"

ag_body = f"""  <nav class="crumbs" aria-label="Laluan">
    <ol><li><a href="/">Laman utama</a></li><li><a href="/blog.html">Blog</a></li><li>The Anxious Generation</li></ol>
  </nav>

  <article>
    <header class="page-head">
      <h1>{AG_TITLE}</h1>
      <p class="lead">{AG_LEDE}</p>
      <p class="article-meta">Oleh <a href="/about.html">{NAME}</a> · <time datetime="2026-10-27">27 Okt 2026</time> · Buku · 5 minit baca</p>
    </header>

    <div class="prose">
      <p class="disclosure">Artikel ini mengandungi pautan affiliate Shopee. Jika anda membeli melaluinya saya
      mungkin menerima komisen kecil tanpa kos tambahan kepada anda. <a href="/disclaimer.html">Baca penafian</a>.</p>

      <div class="note" style="margin-bottom:1.75rem">
        <p><strong>Jawapan ringkas:</strong> saya tak jumpa ayat "frustrate our children everyday" sebiji dalam
        buku <cite>The Anxious Generation</cite>. Tapi maksudnya selari dengan mesej buku tu: biar anak
        berdepan kecewa yang kecil dan sesuai dengan umurnya sambil ibu bapa ada di sisi. Bukan sengaja
        menyakitkan hati anak.</p>
      </div>

      <h2 id="bermula">Bermula dari satu komen di media sosial</h2>
      <p>Baru-baru ni saya terbaca satu komen di sebuah thread. Penulisnya kongsi petikan yang katanya
      dari buku <cite>The Anxious Generation</cite>: <em>"Look for opportunities to frustrate our children
      everyday."</em> Katanya dari situ anak akan belajar kawal emosi sebab dalam dunia ni tak semua yang
      kita nak kita dapat.</p>
      <p>Ayat tu buat saya berhenti sekejap. Sengaja kecewakan anak setiap hari? Bunyinya agak keras.</p>
      <p>Saya sendiri belum ada anak lagi. Tapi ayat ni tetap buat saya terfikir tentang cara saya nak didik
      anak suatu hari nanti. Jadi saya cuba selidik sendiri. Saya baca beberapa sumber dan tanya AI untuk
      faham maksud sebenarnya. Apa yang saya tulis di sini ialah apa yang saya faham sebagai pembaca, bukan
      nasihat daripada ibu bapa yang berpengalaman atau pakar.</p>

      <h2 id="maksud">Apa maksud "frustrate our children"?</h2>
      <p>Selepas difikirkan, maksudnya lebih kepada jangan cepat-cepat buang semua rasa kecewa dari hidup
      anak. Biar dia rasa kecewa yang kecil setiap hari supaya dia belajar urus perasaan tu sendiri.
      Contohnya:</p>
      <ul>
        <li>Anak minta sesuatu, kita jawab "tak boleh" atau "tunggu" dan tak terus mengalah bila dia merengek.</li>
        <li>Biar dia kalah dalam permainan. Jangan sengaja bagi dia menang.</li>
        <li>Bila dia susah nak ikat tali kasut atau siapkan puzzle, jangan terus tolong.</li>
        <li>Biar dia rasa bosan. Jangan terus hulur telefon.</li>
      </ul>
      <p>Yang penting ibu bapa tetap ada di sisi. Iktiraf perasaannya (<em>"Adik marah sebab tak dapat,
      kan?"</em>) tapi jangan ubah keputusan semata-mata sebab dia menangis. Dari situ anak belajar yang
      rasa kecewa boleh ditanggung dan akan berlalu.</p>

      <h2 id="ringkasan">Ringkasan buku The Anxious Generation</h2>
      <p>Buku ni ditulis oleh Jonathan Haidt, ahli psikologi sosial dan profesor di NYU Stern School of
      Business. Ia terbit pada 2024. Rupanya ayat dalam thread tadi bukan teras utama buku ni. Antara isi
      utama yang saya faham:</p>
      <ol>
        <li><strong>"Great Rewiring".</strong> Antara 2010 hingga 2015 zaman kanak-kanak berubah daripada
        berasaskan permainan kepada berasaskan telefon. Haidt kaitkan perubahan ni dengan lonjakan
        kemurungan dan kebimbangan dalam kalangan remaja.</li>
        <li><strong>Terlalu dilindungi di dunia nyata tapi kurang dilindungi di dunia maya.</strong> Ibu bapa
        takut anak main di luar sendirian tapi bebaskan mereka di media sosial. Ayat dalam thread tadi
        paling dekat dengan tema ni.</li>
        <li><strong>Empat norma yang dicadangkan:</strong> tiada telefon pintar sebelum sekolah menengah,
        tiada media sosial sebelum umur 16 tahun, sekolah bebas telefon dan lebih banyak permainan bebas.</li>
      </ol>
      <p>Buku ni ada juga pengkritiknya. Ahli akademik seperti Candice Odgers dan Amy Orben berpendapat data
      yang ada lebih tunjuk kaitan, belum cukup kuat untuk buktikan telefon punca utama. Data dari Asia
      termasuk Malaysia pun sangat sedikit, jadi tak semuanya semestinya terpakai di sini.</p>

      <h2 id="asal-idea">Dari mana datangnya idea "kecewakan anak"?</h2>
      <p>Idea yang paling hampir datang dari <a href="https://www.nowthinkaboutit.com/2011/07/frustrate-your-children-john-rosemond/" target="_blank" rel="noopener">John Rosemond</a>,
      ahli psikologi keluarga dari Amerika. Dia guna istilah "vitamin N", iaitu perkataan "tidak".
      Nasihatnya mudah: beri anak semua yang dia betul-betul perlu tapi hanya lebih kurang 25% daripada apa
      yang dia mahu. Jangan juga buat untuk anak apa yang dia mampu buat sendiri.</p>
      <p>Gordon Neufeld dan Gabor Maté dalam buku <cite>Hold On to Your Kids</cite> pula setuju anak perlu
      berdepan kekecewaan. Cuma ia hanya membina bila anak rasa selamat dan rapat dengan ibu bapa.</p>
      <p>Jadi kemungkinan besar ayat dalam thread tu gabungan idea-idea ni yang disandarkan pada buku Haidt.</p>

      <h2 id="learned-helplessness">Terlalu banyak kecewa boleh buat anak putus asa?</h2>
      <p>Ini soalan yang terus terlintas dalam kepala saya. Jawapannya boleh. Dalam psikologi ada konsep
      <strong>learned helplessness</strong> yang diperkenalkan oleh Martin Seligman. Bila seseorang berulang
      kali gagal tanpa dapat buat apa-apa, dia belajar yang usaha tak ada gunanya lalu berhenti mencuba.</p>
      <p>Saya teringat kisah anak gajah yang diikat pada pancang kecil. Waktu kecil dia memang tak mampu
      lepaskan diri. Bila dah besar dia sebenarnya mampu cabut pancang tu dengan mudah tapi tak pernah cuba
      lagi. Kisah ni cuma perumpamaan tapi ia gambarkan learned helplessness dengan tepat.</p>
      <p>Jadi kuncinya bukan banyak atau sedikit kecewa tapi jenis kecewa tu:</p>
      <ul>
        <li><strong>Ada jalan keluar:</strong> boleh diatasi dengan usaha, contohnya cuba lagi atau tunggu.</li>
        <li><strong>Sesuai dengan umur:</strong> cabaran sedikit di atas kemampuan anak, bukan terlalu jauh.</li>
        <li><strong>Ada sokongan:</strong> ibu bapa ada di sisi bila anak sedang kecewa.</li>
        <li><strong>Seimbang dengan kejayaan:</strong> anak perlu juga rasa berjaya selepas berusaha.</li>
      </ul>
      <p>Kalau anak makin cepat menyerah atau selalu kata "tak guna cuba", itu tanda dosnya terlalu tinggi
      atau sokongannya kurang.</p>

      <h2 id="pengajaran">Apa yang saya bawa pulang</h2>
      <p>Sebagai orang yang belum jadi ayah, ini yang saya simpan untuk masa depan: yang penting bukan
      sekadar anak rasa kecewa tapi <strong>kecewa yang kemudian berjaya diatasi</strong>. Setiap kali anak lalui kitaran "susah, cuba, berjaya" dia bina keyakinan yang usahanya
      bermakna. Itulah yang akan jadikan dia gajah yang berani cabut pancang bila dah besar.</p>
      <p>Satu lagi pengajaran kecil: petikan yang tular di media sosial tak semestinya datang dari buku yang
      disebut. Elok kita semak dulu sebelum kongsi.</p>

      <div class="buybox">
        <h3>Nak baca sendiri?</h3>
        <ul>
          <li><a href="{AG_SHOPEE}" rel="sponsored nofollow noopener" target="_blank"><strong>The Anxious Generation</strong> oleh Jonathan Haidt di Shopee &rarr;</a></li>
        </ul>
        <p style="margin:0.75rem 0 0;font-size:var(--fs-small);color:var(--ink-faint)">Harga di Shopee boleh berubah jadi semak sebelum bayar.</p>
      </div>

      <h2 id="soalan-lazim">Soalan lazim</h2>
      <h3>Siapa penulis buku The Anxious Generation?</h3>
      <p>Jonathan Haidt, ahli psikologi sosial dan profesor di NYU Stern School of Business. Buku ni terbit pada 2024.</p>
      <h3>Betul ke ayat "look for opportunities to frustrate our children" ada dalam buku tu?</h3>
      <p>Saya tak dapat sahkan ayat tu ditulis sebiji begitu. Maksudnya selari dengan tema buku tentang ibu
      bapa yang terlalu melindungi anak. Idea yang paling hampir datang dari John Rosemond.</p>
      <h3>Macam mana nak ajar anak kawal emosi bila kecewa?</h3>
      <p>Biar anak berdepan kecewa yang kecil dan sesuai dengan umurnya. Iktiraf perasaannya dan tetap tegas
      dengan keputusan. Pastikan juga dia selalu rasa berjaya selepas berusaha.</p>
      <h3>Boleh ke terlalu banyak kecewa memudaratkan anak?</h3>
      <p>Boleh. Kecewa yang berulang tanpa jalan keluar atau sokongan boleh buat anak berhenti mencuba. Ini
      dipanggil learned helplessness.</p>

      <h2 id="rujukan">Rujukan</h2>
      <ul>
        <li>Jonathan Haidt, <cite>The Anxious Generation</cite> (2024)</li>
        <li><a href="https://www.nowthinkaboutit.com/2011/07/frustrate-your-children-john-rosemond/" target="_blank" rel="noopener">John Rosemond, "Frustrate Your Children"</a></li>
        <li><a href="https://thriveforchange.com/please-frustrate-your-kids-2/" target="_blank" rel="noopener">Thrive for Change, "Please, frustrate your kids!"</a></li>
        <li>Gordon Neufeld dan Gabor Maté, <cite>Hold On to Your Kids</cite></li>
        <li>Martin Seligman, kajian learned helplessness</li>
      </ul>

      <div class="author">
        <img src="{PHOTO}" width="64" height="64" alt="{NAME}" loading="lazy">
        <p><strong>{NAME}</strong><br>Berkongsi pandangan peribadi tentang buku, media sosial dan keputusan hidup, dari Putrajaya.
        <a href="/about.html">Kenali saya</a>.</p>
      </div>
    </div>
  </article>"""

ag_graph = [WEBSITE, PERSON, {
    "@type": "BlogPosting",
    "@id": f"{AG_URL}#article",
    "headline": AG_TITLE,
    "description": AG_DESC,
    "datePublished": "2026-10-27",
    "dateModified": "2026-10-27",
    "url": AG_URL,
    "mainEntityOfPage": AG_URL,
    "inLanguage": "ms-MY",
    "image": OG,
    "author": {"@id": f"{SITE}/#person"},
    "publisher": {"@id": f"{SITE}/#person"},
    "about": {"@type": "Book", "name": "The Anxious Generation", "author": {"@type": "Person", "name": "Jonathan Haidt"}},
}, {
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Laman utama", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog.html"},
        {"@type": "ListItem", "position": 3, "name": "The Anxious Generation", "item": AG_URL},
    ],
}]

PAGES = [
    (f"blog/{AG_SLUG}.html", AG_TITLE + " | " + NAME, AG_DESC,
     ag_body, dict(graph=ag_graph, og_type="article", active="/blog.html")),
    ("blog/review-buku-atomic-habits-bm.html", f"{AH_TITLE} | {NAME}",
     "Pandangan peribadi tentang buku Atomic Habits: dibaca dalam English, banyak belajar daripada perkongsian versi Bahasa Melayu di media sosial, plus cara elak buku cetak rompak.",
     ah_body, dict(graph=ah_graph, og_type="article", active="/blog.html", og=f"{SITE}/assets/img/og-atomic-habits.png")),
    ("index.html", f"{NAME} — Jurnal Peribadi",
     f"Laman peribadi {NAME} dari Putrajaya: pandangan tentang buku dan media sosial, panduan memilih barang rumah dan cerita tentang keputusan besar hidup.",
     home_body, dict(graph=home_graph, js="/assets/js/prism.js")),
    ("about.html", f"Tentang {NAME}",
     f"Kenali {NAME}, berasal dari Batu Gajah, Perak dan kini menetap di Putrajaya. Menulis tentang keputusan hidup yang betul-betul dilalui.",
     about_body, dict(graph=about_graph, og_type="profile", active="/about.html")),
    ("blog.html", f"Blog — {NAME}",
     f"Semua artikel {NAME}: pandangan tentang buku dan media sosial, panduan barang rumah dan pengalaman peribadi.",
     blog_body, dict(active="/blog.html")),
    ("thought.html", f"Thought — {NAME}",
     f"Kata-kata dan persoalan yang melekat dalam fikiran {NAME} selepas membacanya.",
     thought_body, dict(active="/thought.html")),
    ("privacy.html", f"Dasar privasi — {NAME}",
     "Apa yang ibrahimroslan.com kumpul dan tidak kumpul tentang pelawat.", privacy_body, {}),
    ("disclaimer.html", f"Penafian — {NAME}",
     "Penafian dan pendedahan pautan affiliate di ibrahimroslan.com.", disclaimer_body, {}),
    ("404.html", f"Halaman tidak dijumpai — {NAME}", "Halaman ini tidak wujud.", nf_body,
     dict(robots="noindex")),
    ("blog/_template.html", f"[Tajuk artikel] — {NAME}", "[Ringkasan artikel untuk Google, 120–155 aksara.]",
     tpl_body, dict(graph=tpl_graph, robots="noindex", og_type="article", active="/blog.html")),
]




PAGES.extend(MD_PAGES)

for path, title, desc, body, kw in PAGES:
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(path, title, desc, body, **kw), encoding="utf-8")
    print("wrote", path)

# ====================================================================== SITEMAP & RSS (dijana automatik)
import email.utils as _eu, datetime as _dt
STATIC = ["/", "/about.html", "/blog.html", "/thought.html", "/disclaimer.html", "/privacy.html"]
_sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for _u in STATIC:
    _sm.append(f"  <url><loc>{SITE}{_u}</loc><lastmod>{UPDATED}</lastmod></url>")
for _href, _t, _ex, _iso, _d, _c in POSTS:
    _sm.append(f"  <url><loc>{SITE}{_href}</loc><lastmod>{max(_iso, UPDATED) if _href.endswith('atomic-habits-bm.html') else _iso}</lastmod></url>")
_sm.append("</urlset>")
(OUT / "sitemap.xml").write_text("\n".join(_sm) + "\n", encoding="utf-8")

def _rfc(iso):
    return _eu.format_datetime(_dt.datetime.fromisoformat(iso + "T09:00:00+08:00"))
_items = []
for _href, _t, _ex, _iso, _d, _c in POSTS:
    _items.append(f"""    <item>
      <title>{esc(_t)}</title>
      <link>{SITE}{_href}</link>
      <guid isPermaLink="true">{SITE}{_href}</guid>
      <pubDate>{_rfc(_iso)}</pubDate>
      <category>{esc(_c)}</category>
      <description>{esc(_ex)}</description>
    </item>""")
_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{NAME} — Blog</title>
    <link>{SITE}/</link>
    <description>Satu perkara, beribu perspektif. Pandangan peribadi {NAME} tentang buku, media sosial, barang rumah dan keputusan hidup.</description>
    <language>ms-MY</language>
    <lastBuildDate>{_rfc(POSTS[0][3])}</lastBuildDate>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(_items)}
  </channel>
</rss>
"""
(OUT / "feed.xml").write_text(_feed, encoding="utf-8")
print("wrote sitemap.xml, feed.xml")
