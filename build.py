#!/usr/bin/env python3
"""Generates the static pages in ./public. Run `python3 build.py`, then `npx wrangler deploy`."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent
PUB = ROOT / "public"
SITE = "https://avodahsoft.com"
MAIL = "hello@avodahsoft.com"
APPSTORE = "https://apps.apple.com/app/id6809133057"
KILOJO_STORE = "https://apps.apple.com/app/id6808453483"
UPDATED = "2 October 2026"
YEAR = "2026"
ASSET_VERSION = "20261014h"
# Lector ships from the download bucket, not the App Store; the page states the build it links to.
LECTOR_VERSION = "0.3.0"
LECTOR_SIZE = "252 MB"
LECTOR_DMG = f"https://download.avodahsoft.com/lector/lector-{LECTOR_VERSION}.dmg"

I = {
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M20 6 9 17l-5-5"/></svg>',
    "apple": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 12.53c-.02-2.2 1.8-3.26 1.88-3.31-1.02-1.5-2.62-1.7-3.19-1.72-1.36-.14-2.65.8-3.34.8-.69 0-1.75-.78-2.88-.76-1.48.02-2.85.86-3.61 2.18-1.54 2.67-.39 6.62 1.11 8.79.73 1.06 1.6 2.25 2.75 2.21 1.1-.04 1.52-.71 2.85-.71 1.33 0 1.71.71 2.88.69 1.19-.02 1.94-1.08 2.67-2.15.84-1.23 1.19-2.42 1.21-2.48-.03-.01-2.32-.89-2.34-3.54zM14.88 5.6c.61-.74 1.02-1.77.91-2.8-.88.04-1.94.59-2.57 1.33-.56.65-1.05 1.7-.92 2.7.98.08 1.98-.5 2.58-1.23z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "music": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--orange)"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--orange)"><path d="m12 2 10 5-10 5L2 7l10-5Z"/><path d="m2 12 10 5 10-5"/><path d="m2 17 10 5 10-5"/></svg>',
    "chord": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--purple)"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M8 4v16M13 4v16M3 10h18M3 15h18"/></svg>',
    "gauge": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--teal)"><path d="M12 14 16 8"/><path d="M4 20a8 8 0 1 1 16 0"/><circle cx="12" cy="14" r="1.5"/></svg>',
    "speed": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--blue)"><path d="M4 12h4l3-8 4 16 3-8h2"/></svg>',
    "loop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--orange-2)"><path d="M17 2l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>',
    "lyrics": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--coral)"><path d="M4 6h16M4 12h10M4 18h7"/></svg>',
    "metro": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M9 3h6l3 18H6L9 3Z"/><path d="m12 15 6-9"/></svg>',
    "tuner": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--teal)"><path d="M12 3v18M6 9v6M18 9v6M3 11v2M21 11v2M9 6v12M15 6v12"/></svg>',
    "piano": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--purple)"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 4v10M12 4v10M16 4v10"/></svg>',
    "mic": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--coral)"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0M12 17v5M8 22h8"/></svg>',
    "list": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--blue)"><path d="M8 6h13M8 12h13M8 18h13"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></svg>',
    "bell": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--orange-2)"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10 21a2 2 0 0 0 4 0"/></svg>',
    "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M10 13a5 5 0 0 0 7 0l4-4a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-4 4a5 5 0 0 0 7 7l1-1"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18M8 14h3M13 14h3M8 18h3"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M20 4c-8 0-14 4-15 12 0 2 1 4 3 4 8-1 12-7 12-16Z"/><path d="M5 20c3-5 7-8 12-11"/></svg>',
    "scale": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M12 3v18M5 21h14M6 7h12"/><path d="M6 7 3 13a3 3 0 0 0 6 0L6 7ZM18 7l-3 6a3 3 0 0 0 6 0l-3-6Z"/></svg>',
    "camera": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M3 8a2 2 0 0 1 2-2h2l2-3h6l2 3h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8Z"/><circle cx="12" cy="13" r="4"/></svg>',
    "barcode": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="color:var(--teal)"><path d="M4 5v14M8 5v14M11 5v14M15 5v14M18 5v14M21 5v14"/></svg>',
    "type": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--purple)"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "build": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--orange)"><path d="m14.7 6.3 3 3L7 20H4v-3L14.7 6.3Z"/><path d="m16 5 3 3"/></svg>',
    "ship": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--teal)"><path d="M5 18 3 12l9-3 9 3-2 6"/><path d="M12 9V3"/><path d="M2 21c2 0 3-1 5-1s3 1 5 1 3-1 5-1 3 1 5 1"/></svg>',
    "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--purple)"><path d="M12 3v12"/><path d="m8 11 4 4 4-4"/><path d="M4 17v3h16v-3"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--orange)"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "learn": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 9l10-5 10 5-10 5L2 9Z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9-9-9Z"/><circle cx="8" cy="8" r="1.5"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5Z"/></svg>',
}
# Icons take the colour of the text around them and are hidden from screen readers.
I = {k: re.sub(r' style="[^"]*"', "", v).replace("<svg ", '<svg aria-hidden="true" ', 1) for k, v in I.items()}
ARR = I["arrow"].replace("<svg ", '<svg class="arr" ', 1)
# The company mark: two strokes, one open and one sweeping round to the left.
MARK = "M12 9 24 29M36 9v12c0 11-8 18-23 19"
# The mark (2026-10-14): two strokes, joined, in a seal. The name means both work and service, and
# the mark is two strokes in two weights (mint and white, as the wordmark is Avodah bold and soft
# light) joined into one letter; the seal is a maker's mark, the stamp a craftsman strikes on work
# they stand behind. Never explain it on the site. Drawn once here; the favicon, the home-screen
# icon and the share image are made from the same shapes.
SEAL_RING = 20.6
MARK_AT = "translate(9.6 9.2) scale(.6)"
MARK_A, MARK_B = "M12 9 24 29", "M36 9v12c0 11-8 18-23 19"
MINT, LEAF_TOP, LEAF_BOTTOM = "#A3E6CF", "#12805F", "#08503F"


def logo(uid):
    """The mark as inline SVG. `uid` keeps each copy's gradient id apart on a page."""
    stroke = f'transform="{MARK_AT}" fill="none" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"'
    return (f'<svg viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="lf-{uid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{LEAF_TOP}"/><stop offset="1" stop-color="{LEAF_BOTTOM}"/></linearGradient></defs>'
            f'<circle cx="24" cy="24" r="24" fill="url(#lf-{uid})"/><circle cx="24" cy="24" r="{SEAL_RING}" fill="none" stroke="#fff" stroke-opacity=".32" stroke-width="1.3"/><path d="{MARK_A}" {stroke} stroke="{MINT}"/><path d="{MARK_B}" {stroke} stroke="#fff"/></svg>')


LOGO = logo("nav")

NAV = [("/work", "Apps"), ("/services", "Services"), ("/studio", "Company"), ("/contact", "Contact")]

APPS = {
    "gigpal": {"name": "GigPal", "href": "/gigpal", "icon": "/img/gigpal/icon.png", "live": True, "dark": True,
               "tagline": "The practice room in your pocket.", "shot": ("/img/gigpal/chords.png", "GigPal following the chords of a song")},
    "kilojo": {"name": "Kilojo", "href": "/kilojo", "icon": "/img/kilojo/icon.png", "live": True, "dark": False,
               "tagline": "A food diary that reads your plate.", "shot": ("/img/kilojo/2-snap-your-meal.png", "Kilojo photographing a meal")},
    "papersuite": {"name": "PaperSuite", "href": "/papersuite", "icon": "/img/papersuite/icon.png", "live": False, "dark": False,
                   "tagline": "Every document, in one place.", "shot": ("/img/papersuite/03-notes.png", "PaperSuite notes: due today, pinned and today&rsquo;s reminders")},
    "lector": {"name": "Lector", "href": "/lector", "icon": "/img/lector/icon.png", "live": True, "where": "download", "dark": True,
               "tagline": "The church presenter that listens.", "screen": ("/img/lector/screen.png", "Romans 8:28 on the projector in Lector&rsquo;s Gold Leaf theme")},
}


def head(title, desc, path, image, theme="", extra=""):
    full = title if "Avodahsoft" in title else f"{title} · Avodahsoft"
    ld = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Avodahsoft", "url": SITE, "email": MAIL, "logo": f"{SITE}/favicon.svg",
                     "description": "Avodahsoft designs and builds software for iPhone, iPad, Mac, Windows and the web: custom development for clients, its own apps on the App Store, app acquisitions and training."})
    body = f' class="{theme}"' if theme else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F5F5F2">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:site_name" content="Avodahsoft">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..700&display=swap">{extra}
<link rel="stylesheet" href="/assets/site.css?v={ASSET_VERSION}">
<script type="application/ld+json">{ld}</script>
</head>
<body{body}>
<a class="skip" href="#main">Skip to content</a>'''


def nav(current):
    items = []
    for i, (href, label) in enumerate(NAV):
        cur = ' aria-current="page"' if current == href else ""
        items.append(f'<a href="{href}"{cur} style="--i:{i}">{label}</a>')
    return f'''
<header class="nav">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Avodahsoft home">{LOGO}<span class="wm"><b>Avodah</b>soft</span></a>
    <nav class="links" id="site-menu" aria-label="Primary"><span class="nav-pill" aria-hidden="true"></span>{"".join(items)}</nav>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-menu"><span></span><span></span></button>
  </div>
</header>
<main id="main">'''


FOOT = f'''</main>
<footer class="foot dark">
  <div class="wrap">
    <div class="cols">
      <div class="about">
        <a class="brand" href="/" aria-label="Avodahsoft home">{logo("foot")}<span class="wm"><b>Avodah</b>soft</span></a>
        <p>Avodahsoft designs and builds software for iPhone, iPad, Mac, Windows and the web, for clients and under its own name.</p>
        <a class="mail" href="mailto:{MAIL}">{MAIL}</a>
      </div>
      <div><h4>Apps</h4><a href="/gigpal">GigPal</a><a href="/kilojo">Kilojo</a><a href="/papersuite">PaperSuite</a><a href="/lector">Lector</a><a href="/work">All apps</a></div>
      <div><h4>Company</h4><a href="/services">Services</a><a href="/studio">About</a><a href="/contact">Contact</a><a href="/contact?topic=Support">Support</a></div>
      <div><h4>Legal</h4><a href="/gigpal/privacy">GigPal privacy</a><a href="/gigpal/terms">GigPal terms</a><a href="/kilojo/privacy">Kilojo privacy</a><a href="/kilojo/terms">Kilojo terms</a><a href="/papersuite/privacy">PaperSuite privacy</a><a href="/papersuite/terms">PaperSuite terms</a></div>
    </div>
    <div class="legal"><span>&copy; <span data-year>{YEAR}</span> Avodahsoft. All rights reserved.</span><span>Apple, the App Store, iPhone, iPad and Mac are trademarks of Apple Inc. Windows is a trademark of Microsoft Corporation.</span></div>
  </div>
</footer>
<script src="/assets/site.js?v={ASSET_VERSION}" defer></script>
</body>
</html>
'''


def write(rel, content):
    out = PUB / rel.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def use_webp(html):
    """Points each <img> at the WebP copy of its picture when there is one; link previews keep the PNG."""
    def swap(m):
        return f'{m.group(1)}{m.group(2)}.webp"' if (PUB / (m.group(2).lstrip("/") + ".webp")).is_file() else m.group(0)
    return re.sub(r'(<img [^>]*?src=")(/img/[^"]+)\.png"', swap, html)


def page(path, title, desc, body, current=None, image="/img/og/avodahsoft.png", out=None, theme="", extra=""):
    write(out or (path + ".html" if path != "/" else "/index.html"), use_webp(head(title, desc, path, image, theme, extra) + nav(current) + body + FOOT))


# ---------------------------------------------------------------- building blocks
def chip(live, where="store"):
    if not live:
        return '<span class="chip"><i></i>Coming soon</span>'
    return '<span class="chip live"><i></i>Free for Mac</span>' if where == "download" else '<span class="chip live"><i></i>On the App Store</span>'


def more(label, href=None):
    inner = f"<span>{label}</span>{ARR}"
    return f'<a class="more" href="{href}">{inner}</a>' if href else f'<span class="more">{inner}</span>'


def phone(src, alt="", eager=False, d=None, first=False):
    style = f' style="--d:{d}"' if d is not None else ""
    priority = ' fetchpriority="high"' if first else ""
    return (f'<div class="device"{style}><div class="screen"><img src="{src}" alt="{alt}" width="640" height="1387" '
            f'loading="{"eager" if eager else "lazy"}"{priority} decoding="async"></div></div>')


def mac(src, alt="", eager=False, d=None):
    style = f' style="--d:{d}"' if d is not None else ""
    return f'<div class="monitor"{style}><img src="{src}" alt="{alt}" width="1800" height="1129" loading="{"eager" if eager else "lazy"}" decoding="async"></div>'


def phones(left, centre, right):
    """Three phones on a stage: the middle one first and largest, the outer two drifting faster."""
    return ('<div class="phones">'
            f'<div class="plx side" data-depth="64">{phone(*left, eager=True, d=1)}</div>'
            f'<div class="plx" data-depth="22">{phone(*centre, eager=True, d=0, first=True)}</div>'
            f'<div class="plx side" data-depth="64">{phone(*right, eager=True, d=2)}</div>'
            '</div>')


def macs(main, front):
    return (f'<div class="displays"><div class="plx" data-depth="18">{mac(*main, eager=True, d=0)}</div>'
            f'<div class="float"><div class="plx" data-depth="70">{mac(*front, eager=True, d=1)}</div></div></div>')


def stage(media, app=None, theme=""):
    bar = ""
    if app:
        a = APPS[app]
        bar = (f'<div class="stage-bar"><span class="who"><img src="{a["icon"]}" alt="" width="30" height="30">{a["name"]}{chip(a["live"], a.get("where", "store"))}</span>'
               f'{more("Explore " + a["name"], a["href"])}</div>')
    return f'<div class="stage reveal{" " + theme if theme else ""}">{bar}{media}</div>'


def tile(key, desc):
    a = APPS[key]
    media = mac(*a["screen"]) if "screen" in a else phone(*a["shot"])
    return f'''<a class="tile t-{key}{" dark" if a["dark"] else ""} reveal" href="{a["href"]}">
        <div class="tile-top"><img src="{a["icon"]}" alt="" width="48" height="48" loading="lazy">{chip(a["live"], a.get("where", "store"))}</div>
        <h3>{a["name"]}</h3>
        <p class="tagline">{a["tagline"]}</p>
        <p class="desc">{desc}</p>
        {more("Explore " + a["name"])}
        <div class="tile-media">{media}</div>
      </a>'''


def section_head(kicker, title, lead=None):
    lead_html = f'<p class="lead reveal">{lead}</p>' if lead else ""
    return f'<div class="section-head{"" if lead else " solo"}"><div><p class="kicker reveal">{kicker}</p><h2 class="words">{title}</h2></div>{lead_html}</div>'


def feature(icon, title, text, img=None):
    """A feature tile; with `img` (src, alt) it shows the thing itself above the words, as a product page should."""
    pic = f'<img src="{img[0]}" alt="{img[1]}" width="1200" height="750" loading="lazy" decoding="async">' if img else ""
    return f'<div class="feature{" pic" if img else ""} reveal">{pic}{I[icon]}<h3>{title}</h3><p>{text}</p></div>'


def features(*items, cls=""):
    return f'<div class="features{" " + cls if cls else ""}" data-stagger>' + "".join(feature(*f) for f in items) + "</div>"


def check_list(items):
    return '<ul class="checks">' + "".join(f"<li>{I['check']}<span>{t}</span></li>" for t in items) + "</ul>"


def facts(*items):
    return '<div class="facts" data-stagger>' + "".join(f'<div class="reveal"><b>{n}</b><span>{t}</span></div>' for n, t in items) + "</div>"


def steps(*items):
    return '<div class="steps" data-stagger>' + "".join(f'<div class="step reveal"><span class="n"></span><h3>{t}</h3><p>{p}</p></div>' for t, p in items) + "</div>"


def app_hero(key, title, lead, actions, chips=()):
    a = APPS[key]
    extra = "".join(f'<span class="chip">{c}</span>' for c in chips)
    return f'''
<section class="hero">
  <div class="wrap">
    <div class="app-id reveal"><img src="{a["icon"]}" alt="{a["name"]} app icon" width="60" height="60"><div><p class="name">{a["name"]}</p><div class="chips">{chip(a["live"], a.get("where", "store"))}{extra}</div></div></div>
    <h1 class="display words">{title}</h1>
    <div class="hero-row">
      <p class="lead reveal" style="--i:2">{lead}</p>
      <div class="actions reveal" style="--i:3">{actions}</div>
    </div>
  </div>
</section>'''


def story(kicker, title, body, media):
    return f'''
<section class="section alt story">
  <div class="wrap split">
    <div><p class="kicker reveal">{kicker}</p><h2 class="words">{title}</h2><div class="copy reveal">{body}</div></div>
    <div class="reveal">{media}</div>
  </div>
</section>'''


def trust(title, body, actions, kicker="Privacy"):
    return f'''
<section class="section flush-top">
  <div class="wrap">
    <div class="panel trust reveal">
      <div><p class="kicker">{kicker}</p><h2>{title}</h2></div>
      <div class="body">{body}<div class="actions">{actions}</div></div>
    </div>
  </div>
</section>'''


def closing(kicker, title, lead, actions):
    return f'''
<section class="closing dark">
  <div class="wrap">
    <p class="kicker reveal">{kicker}</p>
    <h2 class="words">{title}</h2>
    <p class="lead reveal">{lead}</p>
    <div class="actions reveal">{actions}</div>
  </div>
</section>'''


def offers(cls=""):
    """What Avodahsoft does: client work, its own products and acquisitions first, then training."""
    return f'''<div class="offers{" " + cls if cls else ""}" data-stagger>
      <a class="offer reveal" href="/services#build"><span class="n">01</span><div><h3>Custom software development</h3><p>We design and engineer apps for iPhone, iPad, Mac, Windows and the web: product strategy, interface design, engineering, backend services and App Store release. Every engagement has a written scope, a fixed price and a working build every week.</p>{more("Start a project")}</div></a>
      <a class="offer reveal" href="/work"><span class="n">02</span><div><h3>Our products</h3><p>We publish our own apps on the App Store. GigPal, Kilojo and Lector are available now, and PaperSuite is on the way. Each is designed, built and supported in-house, to the same standard as our client work.</p>{more("View our apps")}</div></a>
      <a class="offer reveal" href="/services#acquire"><span class="n">03</span><div><h3>App acquisitions</h3><p>Our apps are available to acquire, in whole or in part. Each sale includes the codebase, documentation, store listings and revenue history where it exists, with a managed transition for existing users.</p>{more("Enquire about acquisitions")}</div></a>
    </div>
    <a class="learn reveal" href="/services#training"><span class="n">04</span><div><h3>Training</h3><p>Practical training in app development for individuals and teams, taught from production apps: design, engineering and App Store release.</p></div>{more("Ask about training")}</a>'''


# ---------------------------------------------------------------- home
HOME = f'''
<section class="hero">
  <div class="wrap">
    <p class="kicker reveal">Software company</p>
    <h1 class="display words">We design, build and ship software.</h1>
    <div class="hero-row">
      <p class="lead reveal" style="--i:2">Avodahsoft is a software company working across iPhone, iPad, Mac, Windows and the web. We build products for clients, publish our own apps on the App Store, and offer them for acquisition.</p>
      <div class="actions reveal" style="--i:3"><a class="btn btn-dark" href="/contact?topic=New%20project">Start a project {ARR}</a><a class="btn btn-line" href="/work">View our apps</a></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    {stage(phones(("/img/gigpal/library.png", "GigPal library screen"), ("/img/gigpal/chords.png", "GigPal chord view following a song"), ("/img/gigpal/mixer.png", "GigPal stem mixer with vocals, piano, bass, drums and other")), app="gigpal", theme="t-gigpal")}
    {facts(("2", "apps available on the App Store"), ("4", "products designed and built in-house"), ("5", "platforms: iPhone, iPad, Mac, Windows and the web"), ("End to end", "from first design to App Store release"))}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Services", "Product development, <em>end to end.</em>", "We take software from first design to App Store release, for our clients and for ourselves, and the apps we build are available to acquire.")}
    {offers()}
  </div>
</section>

<section class="section flush-top">
  <div class="wrap">
    {section_head("Products", "Our apps. <em>Designed and built in-house.</em>", "GigPal and Kilojo are on the App Store, Lector is a free download for Mac, and PaperSuite is in App Review.")}
    <div class="tiles" data-stagger>
      {tile("gigpal", "Split any song into vocals, piano, bass, drums and more, follow the chords as they play, change key and tempo, and rehearse with a metronome, tuner and recorder.")}
      {tile("kilojo", "Photograph a meal for calories and macros, scan a barcode for the manufacturer&rsquo;s figures, or enter it by hand. Every number stays editable.")}
      {tile("papersuite", "Notes, scanning, PDF filling and signing, conversion and merging, answers drawn from your own notes, and habits, in one app.")}
      {tile("lector", "Church presentation for Mac that hears the scripture being preached and has the verse on the screens in one tap, then runs the lyrics, slides, videos, stage display and stream. Free.")}
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <p class="kicker reveal">How we work</p>
    <p class="statement words">A written scope. A working build every week. <em>Everything handed over at the end.</em></p>
    <p class="lead reveal statement-lead">Every engagement follows the same process, whether the product is ours or yours.</p>
    {features(
        ("mail", "Direct access", "You deal directly with engineering, without account managers or intermediaries, so decisions are quick and nothing is lost in translation."),
        ("build", "Fixed scope and price", "Screens, states and exclusions are agreed in writing before work begins. The price changes only if the scope does, and only with your approval."),
        ("ship", "Weekly builds", "A working build on your own device every week, so feedback arrives while changes are still inexpensive."),
        ("hand", "Full ownership", "You own the code, accounts and signing keys, with documentation thorough enough for any developer to continue the work."),
        cls="four")}
    <p class="reveal">{more("Our process", "/services")}</p>
  </div>
</section>
{closing("Contact", "Have a project in mind? <em>Let&rsquo;s talk.</em>", "New products, acquisitions, training or support. Every enquiry receives a considered reply, usually within one business day.", f'<a class="btn btn-dark" href="/contact">Get in touch {ARR}</a><a class="btn btn-line" href="mailto:{MAIL}">{MAIL}</a>')}
'''
page("/", "Avodahsoft · Software for iPhone, iPad, Mac, Windows and the web", "Avodahsoft is a software company. We design and build apps for clients, publish our own on the App Store (GigPal, Kilojo, PaperSuite and Lector), and offer them for acquisition.", HOME)

# ---------------------------------------------------------------- gigpal
GIGPAL = f'''{app_hero("gigpal", "Practice like the band is in the room.",
    "GigPal turns any song into a rehearsal. Pull the vocals, piano, bass and drums apart, follow the chords as they change, slow it down, move the key, loop the hard bit, and record yourself over the top.",
    f'<a class="btn btn-dark btn-store" href="{APPSTORE}">{I["apple"]} Download on the App Store</a><a class="btn btn-line" href="#features">See what it does</a>', ["iPhone"])}

<section>
  <div class="wrap">
    {stage(phones(("/img/gigpal/library.png", "GigPal library with demo songs, keys and tempos"), ("/img/gigpal/chords.png", "GigPal chords following the song"), ("/img/gigpal/mixer.png", "GigPal stem mixer with vocals, piano, bass, drums and other")))}
    {facts(("5", "stems per song"), ("3", "chord notations"), ("&plusmn;12", "semitones of key change"), ("0", "ads or trackers"))}
  </div>
</section>

<section class="section dark on-stage" id="film" style="margin-top:clamp(88px,11vw,168px)">
  <div class="wrap">
    <div class="film">
      <div><p class="kicker reveal">See it in action</p><h2 class="words">GigPal <em>in three minutes.</em></h2><p class="lead reveal">Signing in, adding a song, separating the stems, following the chords and building a setlist.</p></div>
      <div class="device film-device reveal"><div class="screen"><video controls playsinline preload="metadata" poster="/img/gigpal/review-poster.jpg"><source src="/gigpal/demo.mp4" type="video/mp4">Your browser cannot play this video. <a href="/gigpal/demo.mp4">Open it directly.</a></video><button class="play" type="button" aria-label="Play the GigPal demo" hidden>{I["play"]}</button></div></div>
    </div>
    <ul class="gallery" data-stagger>
      <li class="reveal">{phone("/img/gigpal/mixer.png", "GigPal stem mixer with vocals, piano, bass, drums and other")}<p class="cap">Stem mixer</p></li>
      <li class="reveal">{phone("/img/gigpal/chords.png", "GigPal chords following the song")}<p class="cap">Chords</p></li>
      <li class="reveal">{phone("/img/gigpal/metronome.png", "GigPal metronome")}<p class="cap">Metronome</p></li>
      <li class="reveal">{phone("/img/gigpal/setlists.png", "GigPal setlists")}<p class="cap">Setlists</p></li>
    </ul>
  </div>
</section>

<section class="section" id="features">
  <div class="wrap">
    {section_head("Features", "One app. <em>The whole practice room.</em>", "Built for gigging musicians, worship teams, choirs, students and anyone who learns songs by ear.")}
    {features(
        ("layers", "Stem mixer", "Separate a song into vocals, piano and keys, bass, drums and everything else. Solo the part you are learning or mute the part you play."),
        ("chord", "Chords that follow the song", "The chord progression is detected on your device and highlighted bar by bar as the song plays. Read it as letters, as numbers (1, 4, 5, 7&flat;) or as solfa."),
        ("gauge", "Key and tempo", "Every song is analysed for key, tempo and beats the moment you add it. Re-analyse in a tap if you disagree, and see it laid out on a piano."),
        ("speed", "Speed and pitch", "Slow a passage to half speed without changing the pitch, or move the whole song into your singing key. Both stay locked to the chords and lyrics."),
        ("loop", "Sections and loops", "GigPal finds the intro, verses and choruses. Tap a section to jump to it or loop it until it is under your fingers."),
        ("lyrics", "Lyrics finder", "Pull in synced lyrics for the song you are working on and follow them as they scroll. Save any lyrics you find, or paste ones you read elsewhere, and edit them later."),
        ("metro", "Metronome", "A rock-solid metronome with tap tempo, count-in, accents and subdivisions, designed to be heard over a full band."),
        ("tuner", "Tuner", "A chromatic tuner with a clear needle and cents readout, accurate to the cent on guitar and bass, low strings included. Works for voice, brass and strings too."),
        ("piano", "Piano and chord keys", "A sampled grand piano on iPhone and iPad. One key plays a whole chord in your key, with pads 1&ndash;8, passing chords and a soft synth pad underneath. Turn the phone sideways for a full keyboard, and solo over chords in two rows."),
        ("mic", "Recorder", "Record yourself over the mix or on its own. Every take is analysed for key and tempo too, so you can see how the rehearsal went."),
        ("list", "Setlists", "Group songs into setlists for a gig or a service, give each set a date and each song a note, reorder by drag, and Play set runs through them in order."),
        ("link", "Play Along", "Paste a YouTube, Spotify, Apple Music or SoundCloud link and play along with the tuner, metronome and piano on top. Every link you play is kept, ready to name."))}
  </div>
</section>
{story("Why GigPal", "Every practice tool. <em>One app.</em>",
    "<p>Musicians usually rehearse with a chord app, a metronome, a tuner and the song open in a browser tab. GigPal brings them together on one screen, keeps them in sync, and stays out of the way while you play.</p>",
    f'<div class="devices">{phone("/img/gigpal/tools.png", "GigPal tools: tuner, metronome, piano, chord finder and more")}{phone("/img/gigpal/tuner.png", "GigPal chromatic tuner")}</div>')}

<section class="section">
  <div class="wrap">
    {section_head("How it works", "From file to rehearsal <em>in a minute.</em>")}
    {steps(
        ("Add a song", "From your files, your camera roll, a link, or a fresh recording. Demo songs are included so you can try everything first."),
        ("Analysed on your phone", "Key, tempo, beats, chords and sections are detected on the device itself. Nothing leaves your phone for this step."),
        ("Separate the stems", "The song is separated in the cloud using the same open-source model family the big apps rely on, then deleted from our servers."),
        ("Practise", "Mix the parts, follow the chords, slow it down, loop it, record yourself. Then add it to the setlist for Sunday."))}
  </div>
</section>

<section class="section flush-top">
  <div class="wrap split top">
    <div><p class="kicker reveal">Pricing</p><h2 class="words" style="margin-top:20px">GigPal is free. <em>Stems included.</em></h2><p class="lead reveal" style="margin-top:24px">Everything that runs on your phone is free. Cloud stem separation costs real computing time, so version 1.0 includes it with a fair-use limit of three songs a day per account. A GigPal Pro plan with a higher allowance is planned for a later update and will be billed through the App Store.</p></div>
    <div class="panel reveal">
      <table class="compare">
        <tr><th>Feature</th><th>Free</th><th>Pro (planned)</th></tr>
        <tr><td>Library, key, tempo, chords, sections</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
        <tr><td>Speed and pitch, loops, lyrics</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
        <tr><td>Metronome, tuner, piano and chord keys, solfa, recorder, Play Along</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
        <tr><td>Setlists, saved lyrics, sync across devices</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
        <tr><td>Stem separation (vocals, piano, bass, drums, other)</td><td class="yes">3 a day</td><td class="yes">More</td></tr>
      </table>
    </div>
  </div>
</section>
{trust("Private by design. <em>Your music stays yours.</em>",
    "<p>No advertising, no analytics SDKs, no tracking. Analysis runs on your device. Songs you separate are uploaded over an encrypted connection, processed, returned to you and deleted from our servers. You can delete your account and everything with it from inside the app.</p>",
    '<a class="btn btn-line" href="/gigpal/privacy">Privacy policy</a><a class="btn btn-line" href="/gigpal/terms">Terms of use</a>')}
'''
page("/gigpal", "GigPal · Practice like the band is in the room", "GigPal is a music practice app for iPhone, iPad and the web: stem separation, chords that follow the song, key and tempo control, metronome, tuner, piano, recorder and setlists.", GIGPAL, current="/work", image="/img/gigpal/icon.png", theme="t-gigpal")

# ---------------------------------------------------------------- lector
DOWNLOAD = f'<a class="btn btn-dark" href="{LECTOR_DMG}">Download for Mac {ARR}</a>'
LECTOR = f'''{app_hero("lector", "The church presenter that listens.",
    "Lector runs the whole service &mdash; lyrics, slides, videos, the stage screen and the stream &mdash; and hears the scripture being preached. &ldquo;Turn with me to Romans eight twenty-eight&rdquo; and the verse is ready, in one tap or on its own. Recognition runs on the Mac; nothing said leaves the room.",
    f'{DOWNLOAD}<a class="btn btn-line" href="#films">See it work</a>', ["Free", "Mac with Apple silicon", "Windows to follow"])}

<section>
  <div class="wrap">
    {stage(macs(("/img/lector/hero.png", "Lector&rsquo;s operator window on a Sunday: the service down the left, the verses heard in the centre, the projector preview and the transcript on the right"), ("/img/lector/screen.png", "Romans 8:28 on the projector in Lector&rsquo;s Gold Leaf theme")))}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {facts(("4", "Bibles on the computer, with no internet at all"), ("8", "screens from one service: projector, choir, lobby, stream"), ("1", "tap from the verse heard to the screens"), ("0", "accounts, logins or tracking"))}
  </div>
</section>

<section class="section" id="features">
  <div class="wrap">
    {section_head("For the media desk", "Built for a volunteer <em>on a Sunday morning.</em>")}
    {features(
        ("mic", "Hears the reference", "&ldquo;Turn with me to Romans eight twenty-eight&rdquo; and the verse is queued before the page is found. A sure reference goes straight to the screens if you ask; the rest wait for one key. In the King James, or the translation named out loud.", ("/img/lector/f-listen.png", "Two verses heard, each a card with the verse, how sure Lector is, Add and Live")),
        ("lyrics", "Follows the reading", "Once a passage is up, the verse being read lights up, the others fade, and the page turns itself. Cautious on purpose: it waits rather than jumps.", ("/img/lector/f-follow.png", "Psalm 23 on the screen with the verse being read lit")),
        ("type", "Catches a quote", "&ldquo;I can do all things through Christ&hellip;&rdquo; with no chapter and verse still finds Philippians 4:13 &mdash; in the King James&rsquo; words or a modern Bible&rsquo;s, a word misheard, or split by a breath.", ("/img/lector/f-quotes.png", "Philippians 4:13 found from its words, with the words heard under it")),
        ("layers", "Up to eight screens", "The projector, the choir&rsquo;s monitor, the lobby and the stream each take a look &mdash; a theme, a text size, which layers to show &mdash; and every screen sees the same service. The stream goes into OBS as a browser source.", ("/img/lector/f-screens.png", "A screen in Settings: its display, look, theme and layout")),
        ("music", "Lyrics, slides and video", "Lyrics pasted once and arranged by part, PowerPoint, Keynote and PDF decks, slides made in Lector, videos and pictures behind the words, walk-in music, and a loop of announcements for the foyer. The stage screen and a phone remote come along.", ("/img/lector/f-songs.png", "A hymn in the centre, its slides in parts")),
        ("calendar", "Plans ahead", "Save an order of service under a name and a day, or drag one onto a calendar. On the morning, the Service column offers it: open, and the whole Sunday is waiting.", ("/img/lector/f-plan.png", "The calendar with three services planned")))}
  </div>
</section>

<section class="section alt" id="films">
  <div class="wrap">
    {section_head("See it work", "A Sunday, <em>in four short films.</em>", "Recorded from the app as it runs. The sermon is spoken, the verses are heard, and nothing is staged after the fact.")}
    <ul class="films" data-stagger>
      <li class="reveal"><div class="monitor film-device"><video playsinline muted loop preload="metadata" poster="/img/lector/hears-the-verse-poster.jpg"><source src="/lector/hears-the-verse.mp4" type="video/mp4">Your browser cannot play this film. <a href="/lector/hears-the-verse.mp4">Open it directly.</a></video><button class="play" type="button" aria-label="Play: Hears the verse." hidden>{I["play"]}</button></div><p class="cap"><b>Hears the verse.</b> &ldquo;Turn with me to Romans eight twenty-eight&rdquo; &mdash; and it is on the screens.</p></li>
      <li class="reveal"><div class="monitor film-device"><video playsinline muted loop preload="metadata" poster="/img/lector/follows-the-reading-poster.jpg"><source src="/lector/follows-the-reading.mp4" type="video/mp4">Your browser cannot play this film. <a href="/lector/follows-the-reading.mp4">Open it directly.</a></video><button class="play" type="button" aria-label="Play: Follows the reading." hidden>{I["play"]}</button></div><p class="cap"><b>Follows the reading.</b> The verse being read lights up; the page turns itself.</p></li>
      <li class="reveal"><div class="monitor film-device"><video playsinline muted loop preload="metadata" poster="/img/lector/quoted-poster.jpg"><source src="/lector/quoted.mp4" type="video/mp4">Your browser cannot play this film. <a href="/lector/quoted.mp4">Open it directly.</a></video><button class="play" type="button" aria-label="Play: Catches a quote." hidden>{I["play"]}</button></div><p class="cap"><b>Catches a quote.</b> No chapter and verse said, and Philippians 4:13 is found from its words.</p></li>
      <li class="reveal"><div class="monitor film-device"><video playsinline muted loop preload="metadata" poster="/img/lector/runs-the-song-poster.jpg"><source src="/lector/runs-the-song.mp4" type="video/mp4">Your browser cannot play this film. <a href="/lector/runs-the-song.mp4">Open it directly.</a></video><button class="play" type="button" aria-label="Play: Runs the song." hidden>{I["play"]}</button></div><p class="cap"><b>Runs the song.</b> Lyrics in parts, each slide drawn as the screens will show it.</p></li>
    </ul>
  </div>
</section>
{story("Why Lector", "The verse should not be late.",
    "<p>Every church has watched a volunteer type a reference while the preacher moves on. Presentation software treats scripture as one more slide to prepare. Lector treats it as something that happens live: it hears the reference, finds the verse and offers it, and the operator&rsquo;s job becomes one keystroke. When the preacher wanders off the plan, the screens still keep up.</p><p>The rest of the service is there too, in one running order: the songs, the announcements, the offering slides, the video. The stage screen shows the speaker the verse, what is next, the notes and a countdown &mdash; on a display, or an iPad on the music stand &mdash; and a phone remote or a Stream Deck drives it from anywhere in the room.</p>",
    mac("/img/lector/bible.png", "Psalm 23 in Lector&rsquo;s Bible tab, with the verses most often read with it underneath"))}
{trust("Private by design. <em>Nothing leaves the room.</em>",
    check_list(["Speech recognition runs on the Mac. The sermon is never sent anywhere to be understood.", "Four Bibles are on the disk and work with no internet: the King James, the American Standard, the Berean Standard and the World English Bible. Licensed translations arrive a verse at a time.", "The sermon write-up is off until the church turns it on, and the switch says plainly what leaves the computer when it does.", "The phone remote and the stage display run over the church&rsquo;s own Wi-Fi, with a PIN.", "Lector backs itself up every day into Documents, and the work comes back on a new computer from one file.", "No account, no analytics, no tracking. Nothing to sign up for."]),
    f'{DOWNLOAD}<a class="btn btn-line" href="/contact?topic=Lector">Ask about Lector {ARR}</a>')}
<section class="section">
  <div class="wrap">
    {section_head("Specifications", "What you <em>need to know.</em>")}
    <dl class="specs reveal">
      <div><dt>Price</dt><dd>Free. No account, no subscription, no ads.</dd></div>
      <div><dt>Requires</dt><dd>macOS 13 or later on a Mac with Apple silicon (M1 or later). Windows to follow.</dd></div>
      <div><dt>Download</dt><dd>{LECTOR_SIZE}. The accurate recogniser (660 MB) downloads once in the background; Listen works before it arrives.</dd></div>
      <div><dt>Bibles included</dt><dd>King James, American Standard, Berean Standard and World English, all offline. Licensed translations arrive a verse at a time; API.Bible and the ESV with the church&rsquo;s own free key.</dd></div>
      <div><dt>Screens</dt><dd>Up to eight: any display on the Mac, and any browser source in OBS, vMix or a TV. A stage display and a phone remote over the church&rsquo;s Wi-Fi.</dd></div>
      <div><dt>Brings in</dt><dd>Lyrics as text, ChordPro or OpenLyrics; PowerPoint, Keynote, PDF and pictures as slides; video, audio and pictures as media.</dd></div>
      <div><dt>Speech</dt><dd>On the Mac, in English, any accent. Nothing recorded, nothing uploaded.</dd></div>
      <div><dt>Backups</dt><dd>Daily, into Documents &rsaquo; Lector Backups, or a folder in iCloud Drive, OneDrive or Google Drive. One file restores a new computer.</dd></div>
    </dl>
  </div>
</section>
{closing("Download", "Free for Mac. <em>Today.</em>",
    f"Lector {LECTOR_VERSION} &middot; {LECTOR_SIZE} &middot; macOS 13 or later on a Mac with Apple silicon. Open the file, drag Lector to Applications, and the first screen sets up the church in a minute. Windows follows.",
    f'{DOWNLOAD}<a class="btn btn-line" href="/contact?topic=Lector">Questions? Write to us {ARR}</a>')}
'''
page("/lector", "Lector · The church presenter that listens", "Lector is a free church presentation app for Mac that runs the whole service — lyrics, slides, videos, the stage screen and the stream — and hears the scripture being preached, so the verse is on the screens the moment it is spoken. Recognition runs on the Mac; nothing leaves the room.", LECTOR, current="/work", image="/img/lector/icon.png", theme="t-lector")

# ---------------------------------------------------------------- papersuite
PAPERSUITE = f'''{app_hero("papersuite", "Every document, in one place.",
    "Write the note. Scan the page, fill in the form, sign the PDF, and ask your own notes what you said last month. Set the reminder beside it, and keep your habits there too. PaperSuite holds every document in one place, on your iPhone and iPad.",
    f'<a class="btn btn-dark" href="/contact?topic=PaperSuite">Notify me at launch {ARR}</a><a class="btn btn-line" href="#features">What it does</a>', ["iPhone", "iPad"])}

<section>
  <div class="wrap">
    {stage(phones(("/img/papersuite/02-pdf-hub.png", "PaperSuite PDF Hub: scan, photos to PDF, merge, sign and convert"), ("/img/papersuite/03-notes.png", "PaperSuite notes: due today, pinned and today&rsquo;s reminders"), ("/img/papersuite/05-ask.png", "PaperSuite Ask: a question answered from your own notes")))}
  </div>
</section>

<section class="section" id="features">
  <div class="wrap">
    {section_head("Notes, documents and habits", "Write it. Scan it. <em>Sign it.</em>", "Notes, PDFs, reminders and habits in one app, so the paperwork of a week stops living in five.")}
    {features(
        ("type", "Notes that keep up", "Headings, checklists, colour and photos as you type. Folders, pins and today&rsquo;s reminders sit at the top, so the note you need is the first one you see. Export any note as text or PDF."),
        ("hand", "Fill in and sign PDFs", "Type into the form, draw your signature once and place it on the page in black or blue ink. It stays a real PDF, ready to send back. Part of PaperSuite Pro."),
        ("layers", "Every PDF tool in one place", "Scan pages with Apple&rsquo;s own document scanner, turn photos into PDFs, merge files, and convert Word, Excel and more."),
        ("lyrics", "Ask your notes anything", "Ask a question with PaperSuite Pro and get an answer drawn only from your own writing. When your notes do not know, it says so instead of making something up."),
        ("bell", "Reminders that ring", "Put a time on anything worth remembering. The reminder rings when it should, and stays beside the note it belongs to."),
        ("check", "Habits and streaks", "Daily check-ins, counted targets and 7, 30, 60 or 90-day challenges, with a month at a glance that shows what you actually did."))}
  </div>
</section>
{story("Why PaperSuite", "One place for everything <em>on paper.</em>",
    "<p>Most of what we keep is paper in some form: the notes from the meeting, the lease to sign, the form to send back, and the reminder to do it by Friday. They usually live in five different apps. PaperSuite keeps them together, on your phone, and lets you ask your own notes what you wrote, with answers drawn only from your writing.</p>",
    f'<div class="devices">{phone("/img/papersuite/01-pdf-editor.png", "Filling in a lease renewal PDF in PaperSuite")}{phone("/img/papersuite/04-note.png", "A PaperSuite note with decisions and a checklist")}</div>')}

<section class="section">
  <div class="wrap">
    {section_head("Beside your notes", "Beside your notes. <em>Reminders, habits and progress.</em>")}
    <ul class="gallery three" data-stagger>
      <li class="reveal">{phone("/img/papersuite/06-reminder.png", "Setting a reminder in PaperSuite")}<p class="cap">Reminders</p></li>
      <li class="reveal">{phone("/img/papersuite/07-habits.png", "PaperSuite habits: today&rsquo;s check-ins and streaks")}<p class="cap">Habits</p></li>
      <li class="reveal">{phone("/img/papersuite/08-progress.png", "PaperSuite progress: the month at a glance")}<p class="cap">Progress</p></li>
    </ul>
  </div>
</section>
{trust("Private by design. <em>Yours, on your phone.</em>",
    check_list(["No account needed. Sign in with Apple only if you want your notes and habits backed up and on your other devices.", "No advertising, no analytics, no tracking software of any kind.", "Scans, photos, PDFs and signatures stay on the phone, and are shared only when you choose to share them.", "Ask AI asks your permission before anything is sent, and sends only what that question needs."]),
    f'<a class="btn btn-dark" href="/contact?topic=PaperSuite">Ask about PaperSuite {ARR}</a><a class="btn btn-line" href="/papersuite/privacy">Privacy policy</a>')}
'''
page("/papersuite", "PaperSuite · Every document, in one place", "PaperSuite is an app for iPhone and iPad for everything on paper: notes with photos and reminders, document scanning, filling in, signing, merging and converting PDFs, questions answered from your own notes, and habits with streaks. Coming soon.", PAPERSUITE, current="/work", image="/img/papersuite/icon.png", theme="t-papersuite")

# ---------------------------------------------------------------- kilojo
KILOJO = f'''{app_hero("kilojo", "A food diary that reads your plate.",
    "Photograph a meal and Kilojo estimates the calories and macronutrients. Scan a barcode and it takes the figures straight off the packet. Everything it produces is editable, because an estimate you cannot correct is a guess you are stuck with.",
    f'<a class="btn btn-dark btn-store" href="{KILOJO_STORE}">{I["apple"]} Download on the App Store</a><a class="btn btn-line" href="/kilojo/privacy">How your data is handled</a>', ["iPhone"])}

<section>
  <div class="wrap">
    {stage(phones(("/img/kilojo/1-today.png", "Kilojo today screen"), ("/img/kilojo/2-snap-your-meal.png", "Kilojo photographing a meal"), ("/img/kilojo/3-progress.png", "Kilojo progress screen")))}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head("Three ways in, and a plan", "Photograph it, scan it, say it. <em>Or plan the week.</em>")}
    {features(
        ("camera", "Point at the plate", "For food that never had a label: a plate of rice, a takeaway, someone else&rsquo;s cooking. Kilojo itemises what it can see and shows its working, so you can see why a number came out as it did."),
        ("barcode", "Read the packet", "A barcode gives the manufacturer&rsquo;s own figures, which beats any estimate from a photograph. Instant, and free to run."),
        ("type", "Or just say it", "Sometimes you know. Type the name and the numbers, and log a repeat of it in one tap for as long as you keep eating it."),
        ("calendar", "Plan the week", "Seven days, four slots each. Pick from meals you have logged or a cookbook of 216 everyday ones, or let Kilojo fill the empty slots to your target and edit what it picked."),
        ("leaf", "Your way of eating", "Vegetarian, vegan, pescatarian, gluten-free, dairy-free, keto, high-protein or low-carb &mdash; every filter has real options for every meal of the day."),
        ("scale", "Where you are heading", "A goal weight with the distance still to go, BMI on the WHO scale for context, and a weight trend that reads the line, not any one morning."))}
  </div>
</section>
{story("Accuracy", "What a photograph <em>cannot tell you.</em>",
    "<p>A picture does not contain the portion. A bowl of rice can hold twice what it appears to, and no amount of cleverness recovers information the camera never captured. Kilojo estimates, and sometimes it is wrong.</p><p>So it is built to be corrected: every figure is editable, it says how confident it is, and it shows the portion it assumed for each item rather than handing down a total. Tell it &ldquo;one cup of rice&rdquo; and the estimate becomes arithmetic. Kilojo is a counting tool, not medical advice.</p>",
    f'<div class="devices">{phone("/img/kilojo/4-plan.png", "Kilojo meal plan for the week")}{phone("/img/kilojo/3-progress.png", "Kilojo progress")}</div>')}
{trust("Private by design. <em>Your diary is yours.</em>",
    check_list(["No advertising, no analytics, no tracking software of any kind.", "Meal photographs are sent for analysis carrying the picture and your typed hint, not your name or email.", "Barcode lookups send the number on the packet and nothing more.", "Erase everything, or delete the account outright, from inside the app. Both reach the server, not just the phone."]),
    '<a class="btn btn-line" href="/kilojo/privacy">Privacy policy</a><a class="btn btn-line" href="/kilojo/terms">Terms of use</a>')}
'''
page("/kilojo", "Kilojo · A food diary that reads your plate", "Kilojo photographs a meal and estimates calories and macros, scans barcodes for the packet's own figures, and keeps every number editable. Available on the App Store for iPhone.", KILOJO, current="/work", image="/img/kilojo/icon.png", theme="t-kilojo")

# ---------------------------------------------------------------- apps (/work)
WORK = f'''
<section class="page-head">
  <div class="wrap">
    <p class="kicker reveal">Apps</p>
    <h1 class="words">Products <em>designed and built in-house.</em></h1>
    <p class="lead reveal" style="--i:2">An app is listed here once it is in testers&rsquo; hands, and marked available once it is on the App Store or ready to download.</p>
  </div>
</section>
<section class="section flush-top">
  <div class="wrap">
    <div class="tiles" data-stagger>
      {tile("gigpal", "Music practice: stem separation, chords, key and tempo, metronome, tuner, piano, recorder and setlists.")}
      {tile("kilojo", "Photo estimates, barcode scanning, a weekly meal plan, and numbers you can always edit.")}
      {tile("papersuite", "Notes, scans and PDFs in one app: fill in, sign, merge and convert documents, with reminders and habits alongside.")}
      {tile("lector", "Church presentation for Mac that hears the scripture being preached and puts the verse on the screens, with lyrics, slides, video, up to eight screens and a stage display. Free.")}
    </div>
  </div>
</section>
{closing("Custom development", "Need an app <em>built to this standard?</em>", "The process behind our own products is available for yours. And if one of these apps is the product you need, it may be available to acquire.", f'<a class="btn btn-dark" href="/contact?topic=New%20project">Start a project {ARR}</a><a class="btn btn-line" href="/contact?topic=Acquisition">Enquire about acquisitions</a>')}
'''
page("/work", "Apps", "The apps Avodahsoft designs, builds and publishes: GigPal and Kilojo on the App Store, PaperSuite in App Review and Lector in development.", WORK, current="/work")

# ---------------------------------------------------------------- services
SERVICES = f'''
<section class="page-head">
  <div class="wrap">
    <p class="kicker reveal">Services</p>
    <h1 class="words">From first idea <em>to the App Store.</em></h1>
    <p class="lead reveal" style="--i:2">We design and build software for clients, offer our own apps for acquisition, and provide practical training in app development.</p>
  </div>
</section>

<section class="section flush-top" id="build">
  <div class="wrap split top">
    <div><p class="kicker reveal">Custom software development</p><h2 class="words" style="margin-top:20px">Your product, <em>designed and built end to end.</em></h2></div>
    <div>
      <p class="lead reveal">We partner with founders and businesses to take an idea from first design to App Store release. Every engagement has a written scope, a fixed price and a working build every week.</p>
      <div class="reveal" style="margin-top:36px">{check_list(["Product strategy and interface design", "Apps for iPhone, iPad, Mac, Windows and the web", "Accounts, sync, subscriptions and payments", "App Store submission, privacy disclosures and review", "Documented handover of code, accounts and signing keys"])}</div>
      <div class="actions reveal" style="margin-top:40px"><a class="btn btn-dark" href="/contact?topic=New%20project">Start a project {ARR}</a></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    {section_head("Process", "Four stages. <em>No surprises.</em>", "Client work remains confidential unless a client chooses otherwise. The process is the same for every engagement.")}
    {steps(
        ("Scope", "Screens, states and exclusions are documented, and a fixed price is agreed against them before work begins."),
        ("Build", "A working build on your own device every week, so issues surface early and decisions stay yours."),
        ("Release", "App Store listing, privacy disclosures and App Review are part of the engagement, not an extra."),
        ("Handover", "You own the repository, accounts and signing keys, documented for any developer to continue."))}
  </div>
</section>

<section class="section" id="acquire">
  <div class="wrap split top">
    <div><p class="kicker reveal">Acquisitions</p><h2 class="words" style="margin-top:20px">Acquire an app <em>outright.</em></h2></div>
    <div>
      <p class="lead reveal">Our apps are available to acquire, in whole or in part. Each sale includes the codebase, documentation, store listings and revenue history where it exists, with a managed transition for existing users.</p>
      <p class="reveal muted" style="margin-top:20px">Enquiries are handled confidentially.</p>
      <div class="actions reveal" style="margin-top:36px"><a class="btn btn-dark" href="/contact?topic=Acquisition">Enquire about acquisitions {ARR}</a><a class="btn btn-line" href="/work">View our apps</a></div>
    </div>
  </div>
</section>

<section class="section flush-top" id="training">
  <div class="wrap">
    <div class="panel split top reveal">
      <div><p class="kicker">Training</p><h2 style="margin-top:20px">Learn to build apps.</h2></div>
      <div>
        <p class="lead">Practical training in software development for individuals and teams, taught from production apps: product design, engineering and App Store release.</p>
        <div class="actions" style="margin-top:36px"><a class="btn btn-dark" href="/contact?topic=Training">Ask about training {ARR}</a></div>
      </div>
    </div>
  </div>
</section>
{closing("Get started", "Tell us about <em>your project.</em>", "Share the idea, the audience and the timeline. We will reply with a clear view of scope, cost and fit.", f'<a class="btn btn-dark" href="/contact?topic=New%20project">Start a project {ARR}</a><a class="btn btn-line" href="mailto:{MAIL}">{MAIL}</a>')}
'''
page("/services", "Services", "Custom software development for iPhone, iPad, Mac, Windows and the web, app acquisitions, and practical training in app development. Written scope, fixed price, weekly builds and full handover.", SERVICES, current="/services")

# ---------------------------------------------------------------- company (/studio)
STUDIO = f'''
<section class="page-head">
  <div class="wrap split">
    <div>
      <p class="kicker reveal">Company</p>
      <h1 class="words">Our work is <em>our service.</em></h1>
      <p class="lead reveal" style="--i:2">Avodah is an old word that means both work and service, and it is how we build: every app made with care for the people who rely on it, and looked after for years. We design and build for iPhone, iPad, Mac, Windows and the web, for clients and under our own name; we offer our apps for acquisition, and we teach people to build their own.</p>
    </div>
    <div class="brand-panel dark reveal" aria-hidden="true">
      {logo("panel")}
      <span class="name wm"><b>Avodah</b>soft</span>
      <span class="means"><span>Work</span><span>Service</span><span>Care</span></span>
    </div>
  </div>
</section>

<section class="section flush-top">
  <div class="wrap">
    {section_head("Principles", "Quality is in <em>the details.</em>", "The empty state, the error message, the second tap that should have been one. Few people notice them, and they decide whether software feels finished. We hold every product to that standard, ours or yours.")}
    {features(
        ("mail", "Direct access", "You deal directly with engineering, without account managers or intermediaries."),
        ("build", "Fixed scope and price", "Scope is agreed in writing before work begins, and the price changes only with your approval."),
        ("ship", "Weekly builds", "Working software on your own device every week, from the first week."),
        ("hand", "Full ownership", "Code, accounts and signing keys are yours, documented for any developer to continue."),
        cls="four")}
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    {section_head("Services", "One company. <em>Four disciplines.</em>")}
    {offers()}
  </div>
</section>
{closing("Contact", "Work <em>with us.</em>", "New products, acquisitions or training. Tell us what you have in mind and you will receive a considered reply, usually within one business day.", f'<a class="btn btn-dark" href="/contact">Get in touch {ARR}</a><a class="btn btn-line" href="/services">Our services</a>')}
'''
page("/studio", "Company", "Avodahsoft is a software company that designs and builds apps for iPhone, iPad, Mac, Windows and the web, for clients and under its own name.", STUDIO, current="/studio")

# ---------------------------------------------------------------- contact
CONTACT = f'''
<section class="page-head">
  <div class="wrap">
    <p class="kicker reveal">Contact</p>
    <h1 class="words">Get <em>in touch.</em></h1>
    <p class="lead reveal" style="--i:2">New products, acquisitions, training or support: every enquiry reaches us directly and receives a considered reply, usually within one business day.</p>
  </div>
</section>
<section class="section flush-top">
  <div class="wrap split top">
    <div class="panel reveal">
      <form class="form" data-contact novalidate>
        <div class="row">
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" placeholder="Your name" autocomplete="name" required minlength="2"></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" placeholder="you@company.com" autocomplete="email" required></div>
        </div>
        <div class="field"><label for="topic">Topic</label><select name="topic" id="topic"><option>New project</option><option>Acquisition enquiry</option><option>Training</option><option>Support · GigPal</option><option>Support · Kilojo</option><option>PaperSuite</option><option>Lector</option><option>Other</option></select></div>
        <div class="field"><label for="f-message">Message</label><textarea id="f-message" name="message" placeholder="For a project: the idea, the audience and the timeline. For support: the app and the device you are using." required minlength="10"></textarea></div>
        <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="send"><button class="btn btn-dark" type="submit">Send message {ARR}</button><span class="status" role="status"></span></div>
        <p class="note">Or email <a href="mailto:{MAIL}">{MAIL}</a>. Your message is used only to reply to you.</p>
      </form>
    </div>
    <div class="topics" data-stagger>
      <div class="reveal"><h3>{I["build"]}Start a project</h3><p>Tell us about the idea, the audience and the timeline. A budget range helps us respond with a realistic proposal, and if we are not the right fit, we will say so.</p></div>
      <div class="reveal"><h3>{I["tag"]}Acquire an app</h3><p>Enquiries about acquiring one of our apps, in whole or in part, are welcome and handled confidentially.</p></div>
      <div class="reveal"><h3>{I["learn"]}Training</h3><p>Tell us your experience and what you want to build, and we will outline how training would work for you.</p></div>
      <div class="reveal"><h3>{I["mail"]}Product support</h3><p>Questions about GigPal, Kilojo, Lector or your account. Include the app and your device, and we will help you resolve it.</p></div>
    </div>
  </div>
</section>
<script>try{{var t=new URLSearchParams(location.search).get('topic');if(t){{t=t.toLowerCase();var s=document.getElementById('topic'),o=[].slice.call(s.options),m=o.find(function(x){{return x.text.toLowerCase()===t}})||o.find(function(x){{return x.text.toLowerCase().indexOf(t)>-1}});if(m)s.value=m.text}}}}catch(e){{}}</script>
'''
page("/contact", "Contact", "New projects, app acquisitions, training, and support for GigPal and Kilojo. Every enquiry receives a considered reply.", CONTACT, current="/contact")

# ---------------------------------------------------------------- legal helpers
def with_contents(body_html):
    """Gives each section heading an id and returns the body with a matching contents list."""
    tag = "h2" if "<h2>" in body_html else "h3"
    toc, used = [], set()

    def anchor(m):
        label = re.sub(r"<[^>]+>", "", m.group(1))
        slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"&[a-z]+;", "", label.lower())).strip("-") or "section"
        base, n = slug, 2
        while slug in used:
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)
        toc.append(f'<a href="#{slug}">{label}</a>')
        return f'<{tag} id="{slug}">{m.group(1)}</{tag}>'

    body_html = re.sub(rf"<{tag}>(.*?)</{tag}>", anchor, body_html, flags=re.S)
    return body_html, "".join(toc)


def legal_page(path, app, kind, intro, body_html, image):
    title = f"{app} {'privacy policy' if kind == 'privacy' else 'terms of use'}"
    other = ("terms", "Terms of use") if kind == "privacy" else ("privacy", "Privacy policy")
    body_html, toc = with_contents(body_html)
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="kicker reveal">{app} · Legal</p>
    <h1 class="words">{'Privacy policy' if kind == 'privacy' else 'Terms of use'}</h1>
    <p class="lead reveal" style="--i:2">{intro}</p>
    <div class="doc-links reveal" style="--i:3"><a class="btn btn-line" href="/{app.lower()}/{other[0]}">{other[1]} {ARR}</a><a class="btn btn-line" href="/{app.lower()}">About {app}</a></div>
  </div>
</section>
<section class="section flush-top">
  <div class="wrap doc">
    <nav class="toc" aria-label="On this page"><p>On this page</p>{toc}</nav>
    <div class="prose">{body_html}</div>
  </div>
</section>'''
    page(path, title, intro, body, image=APPS[app.lower()]["icon"], theme=f"t-{app.lower()}")


def kilojo_legal():
    src = (ROOT / "src" / "kilojo-legal.partial.html").read_text(encoding="utf-8")
    src = re.sub(r"</?mark>", "", src)
    def inner(section_id):
        start = src.index(f'<section id="{section_id}">')
        end = src.find("<section id=", start + 10)
        chunk = src[start: end if end > 0 else len(src)]
        chunk = chunk[chunk.index('<div class="stack prose">') + len('<div class="stack prose">'):]
        chunk = chunk[: chunk.rindex("</section>")]
        chunk = re.sub(r"(\s*</div>){2}\s*$", "", chunk)
        return chunk.replace('class="scroll-x"', 'style="overflow-x:auto"')
    return inner("privacy"), inner("terms")


kp, kt = kilojo_legal()
legal_page("/kilojo/privacy", "Kilojo", "privacy", "Kilojo is a food diary, so it holds things that are genuinely personal: what you eat, what you weigh, and photographs taken in your kitchen. This page says exactly what is held, where it goes and how to get rid of it.", kp, "/img/photos/night.jpg")
legal_page("/kilojo/terms", "Kilojo", "terms", "The short version: Kilojo counts, you stay in charge of the numbers, and it is not medical advice.", kt, "/img/photos/night.jpg")

GP_PRIVACY = f'''
<p class="meta">Last updated {UPDATED} &middot; GigPal for iPhone, iPad and web &middot; Operated by Avodahsoft, Australia</p>
<div class="callout"><b>In one paragraph.</b> GigPal works without an account, and everything that analyses your music (key, tempo, beats, chords, sections) runs on your own device. If you sign in, we hold your email address and a copy of your library metadata so you can sync it. If you use stem separation, the song is uploaded over an encrypted connection, processed, returned to you and deleted from our servers. There is no advertising, no analytics SDK and no tracking, and you can delete your account and everything attached to it from inside the app.</div>

<h2>Who we are</h2>
<p>GigPal is made and operated by Avodahsoft, a software company based in Australia. You can reach us at <a href="mailto:{MAIL}">{MAIL}</a>. We are the data controller for the personal information described here.</p>

<h2>What GigPal stores on your device</h2>
<p>Your library lives on your device: the songs and recordings you add, the analysis results (key, tempo, beats, chords, sections and lyrics timing), any separated stems, your setlists (with their dates and the notes you add to songs), lyrics you save, the streaming links you play in Play Along, and your settings. This information stays on the device unless you sign in and sync, or unless you choose to share something. Saved lyrics, Play Along links, setlist dates and song notes are never uploaded. Deleting a song in the app deletes it and its stems from the device.</p>

<h2>Information we collect when you sign in</h2>
<p>An account is optional. Without one, GigPal does not send us any personal information. If you create an account (by email and password) we store:</p>
<ul>
  <li><b>Account details:</b> your email address, a random account identifier, a display name if you give one, the dates you signed up and last signed in, and a random one-time key used only to let your phone notice that you have confirmed your email.</li>
  <li><b>Library metadata for sync:</b> song titles, artists, keys, tempos, chord, lyrics and section data, setlists (names, notes and running order) and practice settings such as key and speed changes, so your library can be restored on another device. Audio files and recordings are not uploaded for sync. Songs and setlists you delete are removed from sync and marked deleted on our servers; they are erased completely when you delete your account.</li>
  <li><b>Separation usage:</b> how many stem separations each account has run per day, kept for two days to apply the daily fair-use limit. We do not keep the audio.</li>
</ul>
<p>Accounts and synced data are hosted on Supabase infrastructure, protected by per-user access rules so that one account can never read another&rsquo;s data.</p>

<h2>Account emails</h2>
<p>Confirmation, change-of-address and password-reset emails are sent through Resend. Their links open GigPal, or on another device a page on avodahsoft.com that confirms your address when you tap its button. That page sets no cookies and keeps nothing once you close it.</p>

<h2>Stem separation</h2>
<p>When you ask GigPal to separate a song, the audio file is uploaded over HTTPS to our separation service, processed with an open-source source-separation model (Demucs), and the resulting stems are returned to your device. The uploaded file is deleted as soon as processing ends; the stems are deleted once your device has downloaded them, and in any case within 24 hours. We do not listen to, analyse for other purposes, or train models on your audio. Stem separation requires a signed-in account so that we can apply fair-use limits.</p>

<h2>Third-party services you choose to use</h2>
<ul>
  <li><b>Lyrics.</b> When you search for lyrics, the song title and artist you type are sent to LRCLIB (lrclib.net), an open lyrics database. No account information is included.</li>
  <li><b>Google search.</b> &ldquo;Search on Google&rdquo; opens Google in an in-app Safari window. What you search there is between you and Google, under Google&rsquo;s privacy policy; GigPal does not read or collect that page. Lyrics you copy from it and paste into GigPal stay on your device.</li>
  <li><b>Play Along.</b> When you play a YouTube, Spotify, Apple Music or SoundCloud link, it plays inside that service&rsquo;s own embedded player, and GigPal asks the service for the title of the link (its public &ldquo;oEmbed&rdquo; lookup). Those services may set cookies or collect data under their own privacy policies. GigPal does not download, record or store their content.</li>
</ul>

<h2>App updates</h2>
<p>When it starts, GigPal checks Expo&rsquo;s update service for fixes to the app and downloads them. The check includes the app&rsquo;s version and platform; like any web request it reveals your IP address to Expo. It contains no account details or personal information.</p>

<h2>Device permissions</h2>
<ul>
  <li><b>Microphone</b> is used only while the tuner, live chords or recorder screens are open, and stops when you leave them or the app goes to the background. Audio from the microphone is processed on the device and is not sent anywhere unless you separate a recording you made.</li>
  <li><b>Photo library and files</b> are accessed only when you choose a video, an audio file or a profile picture, and only for the item you pick.</li>
  <li><b>Notifications:</b> GigPal does not send notifications. Practice reminders from earlier versions have been retired, and any still scheduled on your device are cancelled.</li>
</ul>

<h2>Purchases</h2>
<p>GigPal is free and contains no in-app purchases. If we add a GigPal Pro subscription in a future update it will be sold through Apple, Apple will process the payment, we will never see your card details, and this policy will be updated before it goes live.</p>

<h2>What we do not do</h2>
<ul>
  <li>No advertising, no advertising identifiers.</li>
  <li>No analytics or tracking SDKs. We do not track you across apps or websites.</li>
  <li>No selling, renting or sharing of personal information with data brokers.</li>
</ul>

<h2>Service providers</h2>
<table><tr><th>Provider</th><th>Purpose</th><th>Data involved</th></tr>
<tr><td>Supabase</td><td>Accounts and database</td><td>Email, account id, synced library metadata</td></tr>
<tr><td>Our separation service (Fly.io hosting)</td><td>Stem separation</td><td>Uploaded audio, temporarily; daily usage counts</td></tr>
<tr><td>Resend</td><td>Account emails (confirmation, change of address, password reset)</td><td>Email address</td></tr>
<tr><td>Cloudflare</td><td>Hosting avodahsoft.com, including the email confirmation page</td><td>Standard web request data</td></tr>
<tr><td>Expo</td><td>App updates</td><td>App version and platform, IP address</td></tr>
<tr><td>Apple</td><td>App distribution</td><td>Handled under Apple&rsquo;s privacy policy</td></tr>
<tr><td>LRCLIB</td><td>Lyrics lookups</td><td>Search terms only</td></tr>
<tr><td>YouTube, Spotify, Apple Music, SoundCloud, Google</td><td>Only when you use Play Along or Search on Google</td><td>Under each service&rsquo;s own privacy policy</td></tr></table>
<p>These providers may process data in the United States and other countries. We choose providers that commit to industry-standard security and data-protection terms.</p>

<h2>Retention and deletion</h2>
<p>You can delete songs, recordings, stems, saved lyrics and Play Along links at any time on the device. You can delete your account from the Profile screen inside the app; this removes your account, synced library data and separation history from our servers, normally immediately and in all cases within 30 days. Uploaded audio for separation is deleted within 24 hours as described above. If you would rather email us to request deletion or a copy of your data, write to <a href="mailto:{MAIL}">{MAIL}</a>.</p>

<h2>Security</h2>
<p>All traffic between the app and our services is encrypted with HTTPS. Your sign-in session is kept in the app&rsquo;s private storage on your device, which other apps cannot read. Database access is restricted with row-level security so that requests are always scoped to the signed-in account, and email links can only sign a phone into the account it asked for. No system is perfectly secure, and we will notify affected users if we become aware of a breach involving their personal information.</p>

<h2>Children</h2>
<p>GigPal is not directed at children under 13 and we do not knowingly collect personal information from them. If you believe a child has created an account, contact us and we will delete it.</p>

<h2>Your rights</h2>
<p>Depending on where you live you may have rights to access, correct, export or delete your personal information, or to object to certain processing. Australian users are covered by the Privacy Act 1988; users in the EU and UK by the GDPR. Most of these rights can be exercised directly in the app; for anything else, email us and we will respond within 30 days.</p>

<h2>Changes</h2>
<p>If this policy changes in a way that matters, we will update the date at the top and tell you inside the app before the change takes effect.</p>
<p><b>Contact:</b> <a href="mailto:{MAIL}">{MAIL}</a></p>
'''
legal_page("/gigpal/privacy", "GigPal", "privacy", "GigPal analyses your music on your own device, works without an account, and never shows ads or tracks you. This page explains the little we do hold, and how to delete it.", GP_PRIVACY, "/img/photos/concert.jpg")

GP_TERMS = f'''
<p class="meta">Last updated {UPDATED} &middot; GigPal for iPhone, iPad and web &middot; Operated by Avodahsoft, Australia</p>
<p>These terms are an agreement between you and Avodahsoft (&ldquo;we&rdquo;, &ldquo;us&rdquo;) covering the GigPal app and the services behind it. By using GigPal you agree to them. If you do not agree, please do not use the app.</p>

<h2>What GigPal is</h2>
<p>GigPal is a practice tool for musicians. It analyses songs you add for key, tempo, chords and structure, lets you change speed and pitch, provides a metronome, tuner, sampled piano with chord keys and a synth pad, recorder, chord finder, sol-fa tools, vocal warm-ups, a lyrics finder, Play Along for streaming links and setlists, and separates songs into stems in the cloud.</p>

<h2>Your music and your responsibility</h2>
<ul>
  <li>You keep all rights to the recordings, songs and other content you add to GigPal. We only use them to provide the service to you.</li>
  <li>You must only import, upload or separate music that you own or have permission to use for this purpose: your own recordings and demos, tracks you have lawfully acquired for personal practice, and material released under licences that allow it. You are responsible for complying with copyright law in your country.</li>
  <li>Stems and other outputs are for your personal practice, study and performance preparation. Do not redistribute, sell or publish separated stems of music you do not own the rights to.</li>
  <li>We may suspend or terminate accounts that misuse the service, including abusive volumes of uploads or clear copyright infringement.</li>
</ul>

<h2>Accounts</h2>
<p>An account is optional for most of GigPal and required for sync and stem separation. Keep your credentials private; you are responsible for activity under your account. You can delete your account at any time from the Profile screen.</p>

<h2>Stem separation and future paid features</h2>
<ul>
  <li>Cloud stem separation is currently free and subject to fair-use limits shown in the app (three songs a day per account, each up to 12 minutes long) so that the service stays fast for everyone. A separation that fails or is cancelled after it starts may still count towards the day&rsquo;s limit. We may adjust limits and features over time.</li>
  <li>If we introduce a paid GigPal Pro plan it will be an auto-renewing subscription purchased through Apple&rsquo;s App Store. Prices will be shown in the app before you buy, renewals and refunds will be handled by Apple under its policies, and these terms will be updated before it launches. Your statutory rights are not affected.</li>
</ul>

<h2>Acceptable use</h2>
<p>Do not attempt to reverse engineer, bypass limits, disrupt or overload the service, access another user&rsquo;s data, or use GigPal for anything unlawful. Automated or bulk use of the separation service is not permitted without our written agreement.</p>

<h2>Third-party services and lyrics</h2>
<p>GigPal can play YouTube, Spotify, Apple Music and SoundCloud links in those services&rsquo; own embedded players, look up lyrics from LRCLIB, and open Google search in an in-app browser. Those services are governed by their own terms, and we do not control their availability or content. GigPal does not download, record or store third-party streamed content. Lyrics you save or paste into GigPal are kept on your device for your personal practice; song lyrics are usually protected by copyright, so do not republish them.</p>

<h2>Accuracy and safety</h2>
<ul>
  <li>Detected keys, tempos, chords, sections and tuner readings are estimates produced by signal analysis. They are usually right and sometimes wrong. Check them with your ears before you rely on them in a performance.</li>
  <li>Protect your hearing: keep playback and headphone volumes at safe levels, especially when using the metronome or looping loud passages.</li>
</ul>

<h2>Availability, updates and changes</h2>
<p>We aim to keep the cloud services running but cannot promise uninterrupted availability. GigPal may download fixes and improvements automatically when it starts. We may change, suspend or discontinue features, and we may update these terms. When a change is significant we will tell you in the app; continuing to use GigPal after that means you accept the updated terms.</p>

<h2>Disclaimer and liability</h2>
<p>GigPal is provided &ldquo;as is&rdquo; to the extent permitted by law. Nothing in these terms excludes rights you have under the Australian Consumer Law or any other consumer protection law that cannot be excluded. Subject to those rights, we are not liable for indirect or consequential loss, and our total liability to you in connection with GigPal is limited to the amount you paid us for the service in the 12 months before the claim arose.</p>

<h2>Termination</h2>
<p>You can stop using GigPal and delete your account at any time. We may suspend or close accounts that breach these terms. On termination your access to the cloud services ends; content stored on your device remains yours.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of Australia, without limiting any mandatory consumer protection you have where you live.</p>
<p><b>Contact:</b> <a href="mailto:{MAIL}">{MAIL}</a></p>
'''
legal_page("/gigpal/terms", "GigPal", "terms", "The short version: your music stays yours, only add music you have the right to use, and cloud stem separation is free with a daily fair-use limit.", GP_TERMS, "/img/photos/concert.jpg")


# ---------------------------------------------------------------- papersuite legal
PAPERSUITE_UPDATED = "7 October 2026"

KP_PRIVACY = f'''
<p class="meta">Last updated {PAPERSUITE_UPDATED} &middot; PaperSuite for iPhone &middot; Operated by Avodahsoft, Australia</p>
<div class="callout"><b>In one paragraph.</b> PaperSuite works without an account, and your notes, PDFs, scans, signatures, photos, reminders and habits are kept on your iPhone. If you choose to sign in with Apple, the text of your notes and your habits are synced to your account so they are backed up and on your other devices; photos and PDFs stay on the phone. If you use Ask AI or the writing tools, the text needed for that request is sent to our server and to Anthropic to produce the answer. We do not keep it, and Anthropic keeps it only briefly for abuse monitoring. There is no advertising, no analytics and no tracking, and you can delete your account and everything synced with it from inside the app.</div>

<h2>Who we are</h2>
<p>PaperSuite is made and operated by Avodahsoft, a software company based in Australia. You can reach us at <a href="mailto:{MAIL}">{MAIL}</a>. We are the data controller for the personal information described here.</p>

<h2>What PaperSuite keeps on your device</h2>
<p>Your notes and folders, reminders, habits and their history, diary entries, PDFs you scan, import or save, signatures you draw, photos you attach to notes and your settings are stored in the app&rsquo;s own storage on your iPhone. iOS encrypts that storage whenever the phone is locked. Unless you sign in, none of it leaves the device, except in iPhone backups (iCloud or a computer) that you control.</p>
<p><b>Locked notes</b> open with Face ID, Touch ID or your passcode through iOS. PaperSuite never receives biometric data. A lock hides a note inside PaperSuite; it is not separate encryption, and a locked note is kept out of exports, search previews, notifications and Ask AI.</p>

<h2>If you sign in</h2>
<p>An account is optional and uses Sign in with Apple. When you sign in we store:</p>
<ul>
  <li><b>Account details:</b> the email address Apple shares with us (which can be Apple&rsquo;s private relay address if you choose to hide yours), your name if you share it or have set one in PaperSuite, an emoji avatar if you choose one, and a random account identifier. A profile photo you choose stays on your device and is not uploaded.</li>
  <li><b>What syncs:</b> the text of your notes (title, body, folder, colour, icon, pin and lock status, dates), your habits, completions and diary entries, and your settings, so they are backed up and available on your other devices.</li>
  <li><b>What does not sync:</b> photos, scans, PDFs and signatures stay on the device. Reminder alerts are scheduled on each device.</li>
</ul>
<p>When you first sign in, what you wrote on the phone before signing in joins your account. Accounts and synced data are held by our database provider, Supabase, on servers in South Korea, protected by per-account access rules so that one account can never read another&rsquo;s data.</p>

<h2>Ask AI and the writing tools</h2>
<p>These features are optional and part of PaperSuite Pro. When you use one, the text needed for that request is sent over HTTPS to our server and from there to Anthropic, whose Claude model writes the answer. For a question, that is the question, up to 12 of your notes (the ones most relevant to it, or your most recent), the names and daily targets of your habits, and the last few questions and answers of the conversation. For the writing tools, it is the note you are working in, any words you selected in it, and your instruction. Ask never includes locked notes; the writing tools send a locked note only when you have opened it and ask them to. The pictures in your notes are never included. The first time you use one of these features, PaperSuite asks your permission before anything is sent, and you can withdraw it at any time in Profile (&ldquo;Allow Ask AI&rdquo;). To count requests against your monthly allowance, our server records how many requests an identifier made each day; that identifier is a random one the app creates for you, or your account if you have signed in. So that one subscription cannot be used to get around the allowance, the server also keeps a daily count for each subscription, identified by the store, the product and the date it was first bought; that count is not linked to an account. We do not store the content of your requests or the answers. Anthropic processes them under its commercial terms, which do not allow it to train models on them, and keeps them only briefly for abuse monitoring.</p>
<p>AI answers can be wrong. PaperSuite never applies one to your notes by itself: it is shown to you first, and nothing changes until you choose.</p>

<h2>PaperSuite Pro and purchases</h2>
<p>PaperSuite Pro is an auto-renewing subscription sold through Apple. Apple processes the payment and we never see your card details. We use RevenueCat to confirm whether a subscription is active: it receives your purchase records from Apple and the app&rsquo;s random identifier, and tells our server whether Pro is active.</p>

<h2>App updates</h2>
<p>When it starts, PaperSuite checks Expo&rsquo;s update service for fixes and downloads them. The check includes the app&rsquo;s version and platform and, like any web request, your IP address. It contains no account details or note content. Updates are signed, and the app refuses one that is not.</p>

<h2>Device permissions</h2>
<ul>
  <li><b>Camera:</b> to scan documents, to read the text on a page into a note (Scan text), and to take photos, only when you choose to. Scan text recognises the words on your iPhone; the page is not sent anywhere and is deleted once read.</li>
  <li><b>Photos:</b> to add pictures to a note or turn them into a PDF, only the ones you pick.</li>
  <li><b>Notifications:</b> for the reminders you set. They are scheduled on your device; a locked note&rsquo;s reminder shows only &ldquo;Note&rdquo;.</li>
  <li><b>Face ID or Touch ID:</b> to open notes you have locked.</li>
</ul>
<p>PaperSuite does not use the microphone or your location.</p>

<h2>What we do not do</h2>
<ul>
  <li>No advertising, no advertising identifiers.</li>
  <li>No analytics or tracking SDKs. We do not track you across apps or websites.</li>
  <li>No selling, renting or sharing of personal information with data brokers.</li>
  <li>We do not use your notes to train AI models, and neither does Anthropic.</li>
</ul>

<h2>Service providers</h2>
<table><tr><th>Provider</th><th>Purpose</th><th>Data involved</th></tr>
<tr><td>Supabase</td><td>Accounts, sync and the server behind Ask AI</td><td>Account details, synced notes and habits, daily AI request counts per identifier and per subscription</td></tr>
<tr><td>Anthropic</td><td>AI answers and writing help</td><td>The text of each request, briefly</td></tr>
<tr><td>Apple</td><td>Sign in with Apple, App Store distribution and payments</td><td>Handled under Apple&rsquo;s privacy policy</td></tr>
<tr><td>RevenueCat</td><td>Subscription status</td><td>Purchase records and a random identifier</td></tr>
<tr><td>Expo</td><td>App updates</td><td>App version and platform, IP address</td></tr>
<tr><td>Cloudflare</td><td>Hosting avodahsoft.com</td><td>Standard web request data; no app data</td></tr></table>
<p>These providers may process data in the United States, South Korea and other countries. We choose providers that commit to industry-standard security and data-protection terms.</p>

<h2>Retention and deletion</h2>
<p>Notes go to Recently Deleted and are removed after 30 days, or straight away if you empty it. You can delete your account from the Profile screen; this permanently removes your account and everything synced with it from our servers at once. If you signed in with Apple, it also revokes PaperSuite&rsquo;s access to your Apple ID, and it asks RevenueCat to delete its record of your identifier. The daily per-subscription AI counts described above, which are not linked to an account, are kept so that deleting an account cannot reset the allowance. Deleting your account does not cancel a PaperSuite Pro subscription: cancel it in your iPhone&rsquo;s Settings, under your name and Subscriptions. What is on the phone is removed when you delete the app; export your notes first if you want a copy. To ask for deletion or a copy of your data by email, write to <a href="mailto:{MAIL}">{MAIL}</a>.</p>

<h2>Security</h2>
<p>All traffic between the app and our services is encrypted with HTTPS. Your sign-in session is kept in the iPhone&rsquo;s keychain, on that device only. Database access is restricted with row-level security so that every request is limited to the signed-in account, and the keys to the AI service never leave our server. No system is perfectly secure, and we will notify affected users if we become aware of a breach involving their personal information.</p>

<h2>Children</h2>
<p>PaperSuite is not directed at children under 13 and we do not knowingly collect personal information from them. If you believe a child has created an account, contact us and we will delete it.</p>

<h2>Your rights</h2>
<p>Depending on where you live you may have rights to access, correct, export or delete your personal information, or to object to certain processing. Australian users are covered by the Privacy Act 1988; users in the EU and UK by the GDPR. Most of these rights can be exercised directly in the app; for anything else, email us and we will respond within 30 days.</p>

<h2>Changes</h2>
<p>If this policy changes in a way that matters, we will update the date at the top and tell you inside the app before the change takes effect.</p>
<p><b>Contact:</b> <a href="mailto:{MAIL}">{MAIL}</a></p>
'''
legal_page("/papersuite/privacy", "PaperSuite", "privacy", "PaperSuite holds your notes, documents and habits, so this page says plainly what stays on your iPhone, what leaves it when you choose, and how to delete it.", KP_PRIVACY, "/img/photos/night.jpg")

KP_TERMS = f'''
<p class="meta">Last updated {PAPERSUITE_UPDATED} &middot; PaperSuite for iPhone &middot; Operated by Avodahsoft, Australia</p>
<p>These terms are an agreement between you and Avodahsoft (&ldquo;we&rdquo;, &ldquo;us&rdquo;) covering the PaperSuite app and the services behind it. By using PaperSuite you agree to them. If you do not agree, please do not use the app.</p>

<h2>What PaperSuite is</h2>
<p>PaperSuite is a notebook for iPhone: notes with photos, reminders and folders; a PDF hub for scanning, converting, merging, filling in, marking up and signing documents; a habit tracker with streaks, challenges and a calendar; and, with PaperSuite Pro, an AI assistant that answers questions about your notes and helps you write.</p>

<h2>Your content</h2>
<ul>
  <li>Everything you write, scan, sign or attach stays yours. We only handle it to provide the service to you, as described in the <a href="/papersuite/privacy">privacy policy</a>.</li>
  <li>Only scan, import or sign documents you are entitled to use.</li>
  <li>PaperSuite keeps your content on your device unless you sign in. Keep backups of anything important, for example with iPhone backups or Export notes. A locked note is hidden behind Face ID; it is not separately encrypted.</li>
</ul>

<h2>Accounts</h2>
<p>An account is optional and uses Sign in with Apple. It adds backup and sync of your notes and habits. You are responsible for activity under your account, and you can delete it at any time from the Profile screen.</p>

<h2>PaperSuite Pro</h2>
<ul>
  <li>PaperSuite Pro is an auto-renewing subscription, monthly or yearly, purchased through Apple&rsquo;s App Store. The price is shown in the app before you buy, and any free trial and its length are shown with it.</li>
  <li>Payment is charged to your Apple ID when you confirm the purchase, or when a free trial ends. The subscription renews automatically unless you turn it off at least 24 hours before the end of the current period, in your iPhone&rsquo;s Settings under your name and Subscriptions. Refunds are handled by Apple under its policies.</li>
  <li>Deleting your account does not cancel a subscription. Your statutory rights are not affected.</li>
  <li>Pro includes a monthly allowance of AI requests, with a daily ceiling, both shown in the app. We may adjust allowances and features over time and will say so in the app.</li>
</ul>

<h2>AI features</h2>
<ul>
  <li>Answers and writing suggestions are produced by an AI model and can be wrong, incomplete or out of date. Check anything that matters before you rely on it. They are not medical, legal, financial or other professional advice.</li>
  <li>PaperSuite shows a suggestion before it changes anything; you decide what to keep.</li>
  <li>Do not use the AI features to create unlawful, harmful or abusive content, or to try to get around their limits.</li>
</ul>

<h2>Signing documents</h2>
<p>PaperSuite lets you draw a signature and place it on a document. It is not a certified electronic-signature service and does not verify identity. Whether a signature made this way is valid for a particular document is for you and the other parties to decide.</p>

<h2>Acceptable use</h2>
<p>Do not attempt to reverse engineer, bypass limits, disrupt or overload the service, access another user&rsquo;s data, or use PaperSuite for anything unlawful. Automated or bulk use of the AI service is not permitted.</p>

<h2>Availability, updates and changes</h2>
<p>We aim to keep the online services running but cannot promise uninterrupted availability; everything on your device keeps working without them. PaperSuite may download fixes and improvements automatically when it starts. We may change, suspend or discontinue features, and we may update these terms. When a change is significant we will tell you in the app; continuing to use PaperSuite after that means you accept the updated terms.</p>

<h2>Disclaimer and liability</h2>
<p>PaperSuite is provided &ldquo;as is&rdquo; to the extent permitted by law. Nothing in these terms excludes rights you have under the Australian Consumer Law or any other consumer protection law that cannot be excluded. Subject to those rights, we are not liable for indirect or consequential loss, including lost notes or documents, and our total liability to you in connection with PaperSuite is limited to the amount you paid us for the service in the 12 months before the claim arose.</p>

<h2>Termination</h2>
<p>You can stop using PaperSuite and delete your account at any time. We may suspend or close accounts that breach these terms. On termination your access to the online services ends; content stored on your device remains yours.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of Australia, without limiting any mandatory consumer protection you have where you live.</p>
<p><b>Contact:</b> <a href="mailto:{MAIL}">{MAIL}</a></p>
'''
legal_page("/papersuite/terms", "PaperSuite", "terms", "The short version: your notes and documents stay yours, Pro is a subscription you can cancel through Apple at any time, and AI answers are suggestions you check.", KP_TERMS, "/img/photos/night.jpg")

# ---------------------------------------------------------------- 404, robots, sitemap, favicon
NOTFOUND = f'''
<section class="page-head not-found">
  <div class="wrap center">
    <p class="kicker reveal">404</p>
    <h1 class="words">That page is <em>not here.</em></h1>
    <p class="lead reveal" style="--i:2">The link may be old. Try the home page, or write to us if you were looking for something specific.</p>
    <div class="actions reveal" style="--i:3"><a class="btn btn-dark" href="/">Go home {ARR}</a><a class="btn btn-line" href="/contact">Contact</a></div>
  </div>
</section>'''
page("/404", "Page not found", "That page is not here.", NOTFOUND, out="/404.html")

write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
paths = ["/", "/gigpal", "/kilojo", "/papersuite", "/lector", "/work", "/services", "/studio", "/contact", "/gigpal/privacy", "/gigpal/terms", "/kilojo/privacy", "/kilojo/terms", "/papersuite/privacy", "/papersuite/terms"]
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{p}</loc></url>\n" for p in paths) + "</urlset>\n")
write("/favicon.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><circle cx="24" cy="24" r="24" fill="#0B6650"/><path d="{MARK_A}" transform="{MARK_AT}" fill="none" stroke="{MINT}" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/><path d="{MARK_B}" transform="{MARK_AT}" fill="none" stroke="#FFFFFF" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
print("done")
