"""Jana gambar kongsi (Open Graph, 1200x630) untuk setiap artikel.

Gambar ini yang muncul bila pautan artikel dikongsi di WhatsApp, Threads, LinkedIn dan lain-lain.
Reka bentuk ikut gaya laman: latar putih hangat, logo IR, tajuk serif dan jalur hijau di bawah.

Cara guna (dari folder repo):  python3 _build/og.py
Perlu: Google Chrome dan Playwright (npx playwright). Jalankan SEBELUM  python3 _build/build.py
kerana build.py hanya guna gambar khas jika fail assets/img/og-<slug>.png wujud.

Artikel baharu: tambah satu baris dalam CARDS di bawah.
"""
import html, pathlib, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = (ROOT / "assets" / "fonts").as_uri()
OUT = ROOT / "assets" / "img"

# (slug artikel, tajuk utama, soalan / baris kedua)
CARDS = [
    ("5-hukum-kebodohan-carlo-cipolla", "5 Hukum Kebodohan Carlo Cipolla", "Bodoh tu sebab IQ atau tindakan?"),
    ("the-anxious-generation-kecewakan-anak", "The Anxious Generation", "Betul ke kita patut sengaja kecewakan anak?"),
    ("review-buku-atomic-habits-bm", "Atomic Habits versi BM", "Berbaloi beli atau tanya AI je?"),
    ("rumah-sewa-kosong-apa-nak-beli-dulu", "Masuk rumah sewa kosong", "Apa nak beli dulu kalau bajet terhad?"),
    ("philips-steam-generator-gc7846-berbaloi", "Philips GC7846", "Berbaloi ganti seterika biasa?"),
    ("vacuum-karcher-wd1s-berbaloi", "Vacuum Karcher WD 1s", "Berbaloi berbanding cordless?"),
    ("peti-ais-toshiba-273l-2-pintu", "Peti ais Toshiba 273L", "Cukup ke untuk bujang dan pasangan?"),
    ("microwave-samsung-23l-jarang-masak", "Microwave Samsung 23L", "Perlu ke kalau jarang masak?"),
    ("rak-besi-boltless-4-tingkat-stor", "Rak besi boltless", "Berbaloi untuk stor rumah sewa?"),
    ("wagon-trolley-lipat-apartmen", "Wagon trolley lipat", "Berbaloi untuk duduk apartmen?"),
    ("toto-atau-tilam-rumah-baru", "Toto atau tilam?", "Mana nak beli dulu bila masuk rumah?"),
    ("water-heater-joven-sl30ip-rs", "Water heater Joven", "Berbaloi ke? Pengalaman awal saya"),
    ("periuk-nasi-giselle-1-2l-bujang", "Periuk nasi Giselle 1.2L", "Cukup ke untuk bujang dan pasangan?"),
]

LOGO = ('<svg viewBox="0 0 64 64" width="84" height="84" aria-hidden="true">'
        '<rect width="64" height="64" rx="16" fill="#1f6b52"/>'
        '<path d="M43 0h5a16 16 0 0 1 16 16v5z" fill="#7cc7a6"/>'
        '<g fill="none" stroke="#fff" stroke-width="6.5" stroke-linecap="square">'
        '<path d="M18 19v27"/><path d="M29.5 46V19h8a8.25 8.25 0 0 1 0 16.5h-8"/><path d="M38 36.5l8 9.5"/></g></svg>')

TEMPLATE = """<!DOCTYPE html>
<html lang="ms"><head><meta charset="utf-8">
<style>
@font-face {{ font-family: "Inter"; font-weight: 100 900; src: url("{fonts}/inter.woff2") format("woff2"); }}
@font-face {{ font-family: "Source Serif 4"; font-weight: 200 900; src: url("{fonts}/source-serif.woff2") format("woff2"); }}
@font-face {{ font-family: "Source Serif 4"; font-style: italic; font-weight: 200 900; src: url("{fonts}/source-serif-italic.woff2") format("woff2"); }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: 1200px; height: 630px; }}
body {{ background: #fbfaf7; color: #1d1d1b; font-family: "Inter", sans-serif; padding: 72px 96px 0;
       display: flex; flex-direction: column; border-bottom: 18px solid #1f6b52; }}
.top {{ display: flex; align-items: center; gap: 22px; }}
.kicker {{ font-size: 26px; font-weight: 600; color: #1f6b52; letter-spacing: 0.01em; }}
h1 {{ margin-top: 54px; font-family: "Source Serif 4", serif; font-weight: 600; font-size: {size}px;
     line-height: 1.08; letter-spacing: -0.015em; text-wrap: balance; }}
.q {{ margin-top: 22px; font-family: "Source Serif 4", serif; font-style: italic; font-size: 44px;
     line-height: 1.2; color: #1f6b52; text-wrap: balance; }}
.foot {{ margin-top: auto; padding-bottom: 44px; font-size: 26px; color: #67675f; }}
.foot b {{ color: #1d1d1b; font-weight: 600; }}
</style></head>
<body>
  <div class="top">{logo}<span class="kicker">Pandangan peribadi</span></div>
  <h1>{title}</h1>
  <p class="q">{question}</p>
  <p class="foot"><b>Ibrahim Roslan</b> · ibrahimroslan.com</p>
</body></html>
"""


def main():
    for slug, title, question in CARDS:
        size = 84 if len(title) <= 24 else 72
        page = TEMPLATE.format(fonts=FONTS, logo=LOGO, size=size,
                               title=html.escape(title), question=html.escape(question))
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(page)
        out = OUT / f"og-{slug}.png"
        subprocess.run(["npx", "--no-install", "playwright", "screenshot", "--channel", "chrome",
                        "--viewport-size=1200,630", "--wait-for-timeout=600",
                        pathlib.Path(f.name).as_uri(), str(out)], check=True)
        pathlib.Path(f.name).unlink()
        try:  # kecilkan saiz fail jika Pillow ada
            from PIL import Image
            Image.open(out).convert("RGB").save(out, optimize=True)
        except ImportError:
            pass
        print("wrote", out.relative_to(ROOT), f"({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
