import html
import json
from pathlib import Path

from PIL import Image

ROOT = Path.home() / "Desktop/Career/fiverr_demos"
IMG = Path(__file__).parent / "img"
e = html.escape

G = [
    dict(d="catalog-watcher", span=7, src="raw/catalog_page.png", box=(0, 0, 0.96, 0.9), name="Catalogue Watch", out="Tracks a shop's prices daily and leads with the drops, struck through in red."),
    dict(d="chrome-extension-page-notes", span=5, src="raw/hero_scene.png", box=(0.4, 0.0, 0.99, 1.0), name="Page Notes", out="A Chrome extension: highlights and notes that come back on every visit."),
    dict(d="ml-forecast-demo", span=5, src="raw/artifact.png", box=(0, 0, 1, 1), name="Larkspur Bakehouse", out="Tomorrow's bake list from a forecast that beats last week by 6.9% to 11.3% error."),
    dict(d="doc-assistant-citations", span=7, src="code/raw/cover_art.png", box=(0.48, 0.0, 1.0, 0.98), name="Blue Harbor Plumbing", out="An assistant that answers from the handbook and cites the page, or says it does not know."),
    dict(d="landing-page-demo", span=12, src="raw/hero_scene.png", box=(0.46, 0.0, 1.0, 1.0), name="Conebook", out="A hand-made landing page for a pottery app, 100 on all four mobile Lighthouse scores."),
    dict(d="ai-agent-automation-demo", span=5, src="code/raw/cover_object.png", box=(0, 0, 1, 1), name="Studio Lind", out="An AI agent that drafts the reply to each lead and waits for a person to approve it."),
    dict(d="wordpress-plugin-demo", span=7, src="raw/calculator.png", box=(0, 0, 1, 0.745), name="Ruiz Window Co.", out="A WordPress quote calculator with an admin inbox, 25 of 25 PHPUnit tests pass."),
    dict(d="stripe-payments-demo", span=5, src="raw/receipt_only.png", box=None, pad=True, name="Fieldnote", out="Stripe checkout and billing kept in step by one signed webhook, 14 of 14 tests."),
    dict(d="data-pipeline-demo", span=7, src="raw/board.png", box=(0.08, 0.0, 0.92, 0.72), name="Copper Kettle", out="Messy shop exports turned into one tested board every morning, 53 of 53 checks."),
    dict(d="python-pdf-extract-demo", span=7, src="raw/split_view.png", box=(0.03, 0.0, 0.96, 0.69), name="Okafor Print Co.", out="Supplier invoices read into a spreadsheet that checks its own math, 19 of 20 straight through."),
    dict(d="discord-bot-demo", span=5, small=True, src="raw/cover_ticket.png", box=(0.5, 0.18, 0.98, 0.86), name="Inkwell & Nib", out="A Discord bot with private tickets and a mod log."),
    dict(d="sheets-automation-demo", span=5, small=True, src="raw/cover_after.png", box=(0, 0, 1, 0.42), name="Halvorsen Office Supply", out="An order export cleaned in Google Sheets, 323 rows to 308."),
]


def theme(d):
    return json.loads((ROOT / d / "brand.json").read_text())["theme"]


def make(g):
    im = Image.open(ROOT / g["d"] / g["src"])
    if g.get("pad"):
        t = theme(g["d"])
        im = im.convert("RGBA")
        bg = Image.new("RGBA", (round(im.width * 1.08), round(im.height * 1.04)), t["canvas"])
        bg.alpha_composite(im, ((bg.width - im.width) // 2, (bg.height - im.height) // 2))
        im = bg
    im = im.convert("RGB")
    if g.get("box"):
        x0, y0, x1, y1 = g["box"]
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    out = []
    for w in (720, 1400) if g["span"] >= 7 else (560, 1100):
        r = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS) if im.width > w else im
        name = f"g-{g['d']}-{r.width}.webp"
        r.save(IMG / name, "WEBP", quality=80, method=6)
        out.append((name, r.width, r.height))
    return out


def font_link(families):
    import urllib.parse
    google = sorted({f["family"] for f in families if not f.get("url")})
    q = "&".join("family=" + urllib.parse.quote_plus(f) + ":wght@" + str(next(x for x in families if x["family"] == f).get("weight", 700)) for f in google)
    links = [f"https://fonts.googleapis.com/css2?{q}&display=swap"] + sorted({f["url"].replace("display=block", "display=swap") for f in families if f.get("url")})
    return "".join(f'<link rel="stylesheet" href="{e(u)}" media="print" onload="this.media=\'all\'">' for u in links)


def section(links_fn):
    tiles, fams = [], []
    for g in G:
        t = theme(g["d"])
        fams.append(t["display"])
        imgs = make(g)
        (n1, w1, h1), (n2, w2, h2) = imgs[0], imgs[-1]
        lk = "".join(f'<a href="{u}">{k}</a>' for k, u in links_fn(g["d"]))
        dark = g["d"] == "discord-bot-demo"
        style = f'--bg:{t["canvas"]};--ink:{t["ink"]};--acc:{t["accent"]};--fd:"{t["display"]["family"]}";--fw:{t["display"].get("weight", 700)}'
        cls = f"g span{g['span']}" + (" small" if g.get("small") else "") + (" wide" if g["span"] == 12 else "") + (" dark" if dark else "")
        tiles.append(f'''<article class="{cls}" style='{style}'><div class="shot"><img src="img/{n1}" srcset="img/{n1} {w1}w, img/{n2} {w2}w" sizes="(min-width: 900px) {max(30, g['span'] * 8)}vw, 100vw" width="{w1}" height="{h1}" alt="{e(g['name'])}" loading="lazy" decoding="async"></div>
<div class="txt"><h3>{e(g['name'])}</h3><p>{e(g['out'])}</p><p class="lk">{lk}</p></div></article>''')
    css = """
.gal{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:22px}
.g{background:var(--bg);color:var(--ink);border-radius:6px;padding:26px 26px 22px;display:flex;flex-direction:column;gap:18px;min-width:0}
.g.span7{grid-column:span 7}.g.span5{grid-column:span 5}.g.span12{grid-column:span 12}
.g .shot{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.g .shot img{display:block;max-width:100%;height:auto;max-height:520px;width:auto;border-radius:4px;box-shadow:0 1px 2px rgba(0,0,0,.08),0 18px 36px -22px rgba(0,0,0,.35)}
.g h3{font-family:var(--fd),Georgia,serif;font-weight:var(--fw);font-size:30px;line-height:1.05;letter-spacing:-.01em;margin:0}
.g .txt p{margin:6px 0 0;font-size:16px;opacity:.86}
.g .lk{display:flex;gap:16px;flex-wrap:wrap;margin-top:12px!important;opacity:1!important;font-weight:600;font-size:15px}
.g .lk a{color:var(--ink);background:linear-gradient(var(--acc),var(--acc)) 0 100%/0 1.5px no-repeat,linear-gradient(color-mix(in srgb,var(--ink) 25%,transparent),color-mix(in srgb,var(--ink) 25%,transparent)) 0 100%/100% 1.5px no-repeat}
.g .lk a:hover{background-size:100% 1.5px,100% 1.5px}
.g.wide{flex-direction:row;align-items:center;gap:40px;padding:34px 40px}
.g.wide .txt{flex:0 0 32%;order:-1}.g.wide h3{font-size:44px}.g.wide .txt p{font-size:18px}
.g.wide .shot img{max-height:560px}
.g.small{flex-direction:row;align-items:center;gap:20px;padding:20px}
.g.small .shot{flex:0 0 46%}.g.small h3{font-size:24px}.g.small .shot img{max-height:200px}
.g.dark .shot img{box-shadow:0 0 0 1px rgba(255,255,255,.06)}
.g.span5.small:first-of-type{}
@media (max-width:900px){.g.span7,.g.span5,.g.span12{grid-column:span 12}.g.wide,.g.small{flex-direction:column;align-items:stretch}.g.wide .txt{order:0}.g.small .shot{flex:none}}
"""
    small_tiles = [t for t, g in zip(tiles, G) if g.get("small")]
    big_tiles = [t for t, g in zip(tiles, G) if not g.get("small")]
    html_out = '<div class="gal">' + "".join(big_tiles[:-1]) + big_tiles[-1] + '<div class="pair">' + "".join(small_tiles) + '</div></div>'
    css += ".pair{grid-column:span 5;display:grid;gap:22px}.pair .g{grid-column:auto}@media (max-width:900px){.pair{grid-column:span 12}}"
    return html_out, css, font_link(fams)
