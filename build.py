#!/usr/bin/env python3
"""Generates the static pages in ./public. Run `python3 build.py`, then `npx wrangler deploy`."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent
PUB = ROOT / "public"
SITE = "https://avodahsoft.com"
MAIL = "hello@avodahsoft.com"
APPSTORE = "https://apps.apple.com/app/id6809133057"
UPDATED = "2 October 2026"
YEAR = "2026"

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
}

NAV = [("/gigpal", "GigPal"), ("/kilojo", "Kilojo"), ("/lector", "Lector"), ("/work", "Work"), ("/studio", "Studio"), ("/contact", "Contact")]


def head(title, desc, path, image):
    full = title if "Avodahsoft" in title else f"{title} · Avodahsoft"
    ld = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Avodahsoft", "url": SITE, "email": MAIL, "logo": f"{SITE}/favicon.svg"})
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0A0E1F">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:site_name" content="Avodahsoft">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>'''


def nav(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if current == h else ""}>{t}</a>' for h, t in NAV)
    return f'''
<header class="nav">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Avodahsoft home"><span class="mark">A</span>Avodahsoft</a>
    <nav class="links" aria-label="Primary">{links}</nav>
    <button class="burger" aria-label="Menu" aria-expanded="false">Menu</button>
  </div>
</header>
<main>'''


FOOT = f'''</main>
<footer>
  <div class="wrap">
    <div>
      <a class="brand" href="/"><span class="mark">A</span>Avodahsoft</a>
      <p class="mt-16">An independent software studio in Australia. Apps for musicians and everyday life, built to be finished rather than merely working.</p>
      <p class="mt-8"><a href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
    <div><h4>Apps</h4><a href="/gigpal">GigPal</a><a href="/kilojo">Kilojo</a><a href="/papersuite">PaperSuite</a><a href="/lector">Lector</a><a href="/work">All work</a></div>
    <div><h4>Studio</h4><a href="/studio">About</a><a href="/contact">Contact</a><a href="/contact?topic=Support">Support</a></div>
    <div><h4>Legal</h4><a href="/gigpal/privacy">GigPal privacy</a><a href="/gigpal/terms">GigPal terms</a><a href="/kilojo/privacy">Kilojo privacy</a><a href="/kilojo/terms">Kilojo terms</a><a href="/papersuite/privacy">PaperSuite privacy</a><a href="/papersuite/terms">PaperSuite terms</a></div>
    <div class="legal"><span>&copy; <span data-year>{YEAR}</span> Avodahsoft. All rights reserved.</span><span>Apple, the App Store and iPhone are trademarks of Apple Inc.</span></div>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


def write(rel, content):
    out = PUB / rel.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def page(path, title, desc, body, current=None, image="/img/photos/stage.jpg", out=None):
    write(out or (path + ".html" if path != "/" else "/index.html"), head(title, desc, path, image) + nav(current) + body + FOOT)


def feature(icon, title, text):
    return f'<div class="card reveal"><div class="icon">{I[icon]}</div><h3>{title}</h3><p>{text}</p></div>'


def check_list(items):
    return '<ul class="feature-list">' + "".join(f"<li>{I['check']}<span>{t}</span></li>" for t in items) + "</ul>"


# ---------------------------------------------------------------- home
HOME = f'''
<section class="hero">
  <div class="photo" style="background-image:url(/img/photos/stage.jpg)"></div><div class="bg"></div>
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow-row"><span class="eyebrow">Independent software studio · Australia</span></div>
      <h1>Software that feels <span class="accent">alive in your hands.</span></h1>
      <p class="lead mt-24">We design and build apps for iPhone, iPad and the web. Our own products first, released under our own name, plus select client work for people who want it made properly rather than quickly.</p>
      <div class="cta">
        <a class="btn primary" href="/gigpal">Meet GigPal {I["arrow"]}</a>
        <a class="btn ghost" href="/contact?topic=New%20project">Start a project</a>
      </div>
      <div class="stats"><div><b>2</b>apps in the pipeline</div><div><b>{YEAR}</b>founded</div><div><b>iOS · Web</b>platforms</div><div><b>1 inbox</b>you talk to the builder</div></div>
    </div>
    <div class="phones"><div class="glow"></div>
      <div class="phone back"><img src="/img/gigpal/chords.png" alt="GigPal chord view following a song" loading="eager"></div>
      <div class="phone front"><img src="/img/gigpal/library.png" alt="GigPal library screen" loading="eager"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Our apps</span><h2 class="mt-8">Four apps, one standard.</h2><p class="lead">Each one is built by the person who answers your email, and each ships when it is genuinely finished.</p></div>
    <div class="grid g2">
      <a class="card product-card reveal" href="/gigpal">
        <div class="media"><img src="/img/photos/band.jpg" alt="A band rehearsing on stage" loading="lazy"><img class="shot" src="/img/gigpal/library.png" alt=""></div>
        <div class="body"><div class="eyebrow-row"><span class="pill"><span class="dot"></span>On the App Store</span><span class="pill">iPhone</span></div><h3>GigPal</h3><p>The practice room in your pocket. Split any song into vocals, piano, bass, drums and more, follow the chords as they play, change key and tempo, and rehearse with a metronome, tuner and recorder.</p><span class="btn primary">Explore GigPal {I["arrow"]}</span></div>
      </a>
      <a class="card product-card reveal" href="/kilojo">
        <div class="media"><img src="/img/photos/night.jpg" alt="A table set for dinner in the evening" loading="lazy"><img class="shot" src="/img/kilojo/2-snap-your-meal.png" alt=""></div>
        <div class="body"><div class="eyebrow-row"><span class="pill"><span class="dot"></span>Coming soon</span><span class="pill">iOS</span></div><h3>Kilojo</h3><p>A food diary that reads your plate. Photograph a meal for calories and macros, scan a barcode for the packet&rsquo;s own figures, or simply type it in. Every number stays editable.</p><span class="btn green">Explore Kilojo {I["arrow"]}</span></div>
      </a>
      <a class="card product-card reveal" href="/papersuite">
        <div class="media"><img src="/img/photos/night.jpg" alt="A quiet desk in the evening" loading="lazy"><img class="shot" src="/img/kepta/today.png" alt=""></div>
        <div class="body"><div class="eyebrow-row"><span class="pill"><span class="dot"></span>Coming soon</span><span class="pill">iPhone</span></div><h3>PaperSuite</h3><p>Every document, in one place. Write notes, scan pages, fill in and sign PDFs, merge and convert them, ask your own notes a question, and keep your habits beside it all.</p><span class="btn primary">Explore PaperSuite {I["arrow"]}</span></div>
      </a>
      <a class="card product-card reveal" href="/lector">
        <div class="media"><img src="/img/photos/stage.jpg" alt="A church stage under lights" loading="lazy"><img class="shot wide" src="/img/lector/screen.png" alt=""></div>
        <div class="body"><div class="eyebrow-row"><span class="pill"><span class="dot"></span>Coming soon</span><span class="pill">Mac</span></div><h3>Lector</h3><p>The verse, the moment it is spoken. Lector listens to the preacher and puts the scripture on the screens as it is read &mdash; with songs, slides, videos, four screens and a stage display for the rest of the service.</p><span class="btn primary">Explore Lector {I["arrow"]}</span></div>
      </a>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">What we do</span><h2 class="mt-8">Build. Ship. Hand over.</h2></div>
    <div class="grid g3">
      {feature("build", "We build your app", "You have the idea and know the market. We handle design, development, App Store submission and the first release. Fixed scope, fixed price, and something working in your hands every week.")}
      {feature("ship", "We run our own", "Products released under the studio&rsquo;s name and supported by the person who wrote them. No ticket queue. You email the studio and the studio answers.")}
      {feature("hand", "We hand over properly", "When an app finds the right owner: a clean codebase, documented handover, whatever revenue history exists, and a transition long enough that nothing breaks on your watch.")}
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="band reveal"><img src="/img/photos/mixer.jpg" alt="Hands on a mixing console" loading="lazy">
      <div><span class="eyebrow">Approach</span><h3 class="mt-8">Finished, not merely working.</h3><p>Most software ships at the point it stops erroring. We are interested in the part after that: the copy that says what it means, the state nobody planned for, the second tap that should have been one. You deal with the person doing the work, and the work is done in the open.</p><a class="btn ghost mt-24" href="/studio">About the studio {I["arrow"]}</a></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap center reveal">
    <h2>Have something in mind?</h2>
    <p class="lead mt-16" style="margin-inline:auto">Support, a new project or an acquisition enquiry. Everything reaches the same inbox and gets a real reply, usually the same day.</p>
    <div class="cta mt-24" style="justify-content:center;display:flex;gap:12px;flex-wrap:wrap"><a class="btn primary" href="/contact">Get in touch {I["arrow"]}</a><a class="btn ghost" href="mailto:{MAIL}">{MAIL}</a></div>
  </div>
</section>
'''
page("/", "Avodahsoft · Apps for musicians, churches and everyday life", "Avodahsoft is an independent software studio in Australia building GigPal, the music practice app, Kilojo, the food diary that reads your plate, PaperSuite, the habit tracker with notes built in, and Lector, the church presentation app that puts the verse on screen as it is spoken.", HOME)

# ---------------------------------------------------------------- gigpal
GIGPAL = f'''
<section class="hero">
  <div class="photo" style="background-image:url(/img/photos/concert.jpg)"></div><div class="bg"></div>
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow-row"><img class="appicon" src="/img/gigpal/icon.png" alt="GigPal app icon" width="64" height="64"><span class="pill"><span class="dot"></span>Now on the App Store</span><span class="pill">iPhone</span></div>
      <h1>Practice like <span class="accent">the band is in the room.</span></h1>
      <p class="lead mt-24">GigPal turns any song into a rehearsal. Pull the vocals, piano, bass and drums apart, follow the chords as they change, slow it down, move the key, loop the hard bit, and record yourself over the top.</p>
      <div class="cta"><a class="btn primary" href="{APPSTORE}">{I["apple"]} Download on the App Store</a><a class="btn ghost" href="#features">See what it does</a></div>
      <div class="stats"><div><b>5</b>stems per song</div><div><b>3</b>chord notations</div><div><b>&plusmn;12</b>semitones of key change</div><div><b>0</b>ads or trackers</div></div>
    </div>
    <div class="phones"><div class="glow"></div>
      <div class="phone back"><img src="/img/gigpal/mixer.png" alt="GigPal stem mixer with vocals, piano, bass, drums and other" loading="eager"></div>
      <div class="phone front"><img src="/img/gigpal/chords.png" alt="GigPal chords following the song" loading="eager"></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">See it in action</span><h2 class="mt-8">Three minutes, start to finish.</h2><p class="lead">Signing in, adding a song, separating the stems, following the chords and building a setlist.</p></div>
    <div class="video reveal"><video controls playsinline preload="metadata" poster="/img/gigpal/review-poster.jpg"><source src="/gigpal/demo.mp4" type="video/mp4">Your browser cannot play this video. <a href="/gigpal/demo.mp4">Open it directly.</a></video></div>
    <div class="gallery reveal">
      <img src="/img/gigpal/library.png" alt="GigPal library with demo songs, keys and tempos" loading="lazy">
      <img src="/img/gigpal/tools.png" alt="GigPal tools: tuner, metronome, piano, chord finder and more" loading="lazy">
      <img src="/img/gigpal/metronome.png" alt="GigPal metronome" loading="lazy">
      <img src="/img/gigpal/setlists.png" alt="GigPal setlists" loading="lazy">
    </div>
  </div>
</section>

<section class="section" id="features">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Everything a rehearsal needs</span><h2 class="mt-8">One app, the whole practice room.</h2><p class="lead">Built for gigging musicians, worship teams, choirs, students and anyone who learns songs by ear.</p></div>
    <div class="grid g3">
      {feature("layers", "Stem mixer", "Separate a song into vocals, piano and keys, bass, drums and everything else. Solo the part you are learning or mute the part you play.")}
      {feature("chord", "Chords that follow the song", "The chord progression is detected on your device and highlighted bar by bar as the song plays. Read it as letters, as numbers (1, 4, 5, 7&flat;) or as solfa.")}
      {feature("gauge", "Key and tempo", "Every song is analysed for key, tempo and beats the moment you add it. Re-analyse in a tap if you disagree, and see it laid out on a piano.")}
      {feature("speed", "Speed and pitch", "Slow a passage to half speed without changing the pitch, or move the whole song into your singing key. Both stay locked to the chords and lyrics.")}
      {feature("loop", "Sections and loops", "GigPal finds the intro, verses and choruses. Tap a section to jump to it or loop it until it is under your fingers.")}
      {feature("lyrics", "Lyrics finder", "Pull in synced lyrics for the song you are working on and follow them as they scroll. Save any lyrics you find, or paste ones you read elsewhere, and edit them later.")}
      {feature("metro", "Metronome", "A rock-solid metronome with tap tempo, count-in, accents and subdivisions, designed to be heard over a full band.")}
      {feature("tuner", "Tuner", "A chromatic tuner with a clear needle and cents readout, accurate to the cent on guitar and bass, low strings included. Works for voice, brass and strings too.")}
      {feature("piano", "Piano and chord keys", "A sampled grand piano on iPhone and iPad. One key plays a whole chord in your key, with pads 1&ndash;8, passing chords and a soft synth pad underneath. Turn the phone sideways for a full keyboard, and solo over chords in two rows.")}
      {feature("mic", "Recorder", "Record yourself over the mix or on its own. Every take is analysed for key and tempo too, so you can see how the rehearsal went.")}
      {feature("list", "Setlists", "Group songs into setlists for a gig or a service, give each set a date and each song a note, reorder by drag, and Play set runs through them in order.")}
      {feature("link", "Play Along", "Paste a YouTube, Spotify, Apple Music or SoundCloud link and play along with the tuner, metronome and piano on top. Every link you play is kept, ready to name.")}
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="band reveal"><img src="/img/photos/singer.jpg" alt="A singer performing under stage lights" loading="lazy">
      <div><span class="eyebrow">Why we built it</span><h3 class="mt-8">Made by a musician who was tired of switching apps.</h3><p>Chords in one app, a metronome in another, a tuner in a third, and the actual song in a browser tab. GigPal puts them on one screen, keeps them in sync, and stays out of your way when you are playing.</p></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">How it works</span><h2 class="mt-8">From file to rehearsal in a minute.</h2></div>
    <div class="grid g4 steps">
      <div class="step reveal"><h3>Add a song</h3><p class="mt-8 dim">From your files, your camera roll, a link, or a fresh recording. Demo songs are included so you can try everything first.</p></div>
      <div class="step reveal"><h3>Analysed on your phone</h3><p class="mt-8 dim">Key, tempo, beats, chords and sections are detected on the device itself. Nothing leaves your phone for this step.</p></div>
      <div class="step reveal"><h3>Separate the stems</h3><p class="mt-8 dim">The song is separated in the cloud using the same open-source model family the big apps rely on, then deleted from our servers.</p></div>
      <div class="step reveal"><h3>Practise</h3><p class="mt-8 dim">Mix the parts, follow the chords, slow it down, loop it, record yourself. Then add it to the setlist for Sunday.</p></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grid g2" style="align-items:start">
      <div class="reveal"><span class="eyebrow">Pricing</span><h2 class="mt-8">GigPal is free. Stems included.</h2><p class="lead mt-16">Everything that runs on your phone is free. Cloud stem separation costs real computing time, so version 1.0 includes it with a fair-use limit of three songs a day per account. A GigPal Pro plan with a higher allowance is planned for a later update and will be billed through the App Store.</p></div>
      <div class="card reveal" style="padding:10px 18px">
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
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="card reveal" style="display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:start"><div class="icon" style="margin:0">{I["shield"]}</div>
      <div><h3>Your music stays yours.</h3><p class="mt-8">No advertising, no analytics SDKs, no tracking. Analysis runs on your device. Songs you separate are uploaded over an encrypted connection, processed, returned to you and deleted from our servers. You can delete your account and everything with it from inside the app.</p><p class="mt-16"><a class="btn ghost" href="/gigpal/privacy">Privacy policy</a> &nbsp; <a class="btn ghost" href="/gigpal/terms">Terms of use</a></p></div>
    </div>
  </div>
</section>
'''
page("/gigpal", "GigPal · Practice like the band is in the room", "GigPal is a music practice app for iPhone, iPad and the web: stem separation, chords that follow the song, key and tempo control, metronome, tuner, piano, recorder and setlists.", GIGPAL, current="/gigpal", image="/img/photos/concert.jpg")

# ---------------------------------------------------------------- lector
LECTOR = f'''
<section class="hero">
  <div class="photo" style="background-image:url(/img/photos/stage.jpg)"></div><div class="bg" style="background:radial-gradient(900px 500px at 15% 10%,rgba(226,185,90,.22),transparent 60%),radial-gradient(700px 500px at 85% 20%,rgba(255,138,61,.14),transparent 60%)"></div>
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow-row"><img class="appicon" src="/img/lector/icon.png" alt="Lector app icon" width="64" height="64"><span class="pill"><span class="dot"></span>Coming soon</span><span class="pill">Mac</span><span class="pill">Windows to follow</span></div>
      <h1>The verse, <span class="accent" style="background:linear-gradient(90deg,#E2B95A,#FF8A3D);-webkit-background-clip:text;background-clip:text">the moment it is spoken.</span></h1>
      <p class="lead mt-24">Lector listens to the preacher and puts the scripture on the screens as it is read &mdash; no typing, no hunting, no verse three sentences late. Then it runs the rest of the service: songs with arrangements, slides, videos, announcements for the lobby, a stage display for the preacher and a remote for a phone. Recognition happens on the Mac; nothing leaves the room.</p>
      <div class="cta"><a class="btn primary" href="/contact?topic=Lector">Tell me when it launches {I["arrow"]}</a><a class="btn ghost" href="#features">What it does</a></div>
    </div>
    <div class="screens"><div class="glow"></div>
      <div class="screen back"><img src="/img/lector/operator.png" alt="Lector&rsquo;s operator window: the live transcript, the queue, the verses it heard, and the preview" loading="eager"></div>
      <div class="screen front"><img src="/img/lector/screen.png" alt="Philippians 4:13 on the projector in Lector&rsquo;s Gold Leaf theme" loading="eager"></div>
    </div>
  </div>
</section>

<section class="section" id="features">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">For the media desk</span><h2 class="mt-8">Built for a volunteer on a Sunday morning.</h2></div>
    <div class="grid g3">
      {feature("mic", "Hears the reference", "&ldquo;Turn with me to Romans eight twenty-eight&rdquo; and the verse is queued before the page is found. Confident references go straight to the screen if you ask; the rest wait for one key.")}
      {feature("lyrics", "Follows the reading", "As the passage is read, the verse being read lights up and the page turns itself. Nineteen translations are built in; licensed ones link in with a key.")}
      {feature("layers", "Four screens, one service", "The projector, the choir&rsquo;s monitor, the stream and the lobby each take a look &mdash; what to show, what to leave out &mdash; and every screen sees the same service.")}
    </div>
    <div class="grid g3 mt-24">
      {feature("music", "Songs, slides and videos", "Lyrics with arrangements, PowerPoint, Keynote and PDF decks, videos, a camera behind the words, a memory stick of walk-in music, and a loop of announcements for the foyer.")}
      {feature("list", "A stage that tells the truth", "The preacher&rsquo;s screen shows the verse, what is next, the notes, a countdown and a word from the desk &mdash; on a display, or an iPad on the music stand.")}
      {feature("bell", "One key, several things", "Moments fire the logo, the countdown and the loop together; schedules fire them by the clock; a phone remote and a Stream Deck do the rest from anywhere in the room.")}
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="product card reveal">
      <div class="copy"><span class="eyebrow">Honestly</span><h2 class="mt-8" style="font-size:clamp(26px,3vw,38px)">The verse should not be late.</h2><p class="lead mt-16" style="font-size:17px">Every church has watched a volunteer type a reference while the preacher moves on. Presentation software treats scripture as one more slide to prepare. Lector treats it as something that happens live: it hears the reference, finds the verse and offers it, and the operator&rsquo;s job becomes one keystroke. When the preacher wanders off the plan, the screen still keeps up.</p></div>
      <div class="shots"><div class="screen"><img src="/img/lector/operator.png" alt="Lector operator window" loading="lazy"></div></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="card reveal" style="display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:start"><div class="icon" style="margin:0">{I["shield"]}</div>
      <div><h3>Nothing leaves the room.</h3>{check_list(["Speech recognition runs on the Mac. The sermon is never sent anywhere to be understood.", "The Bibles are on the disk: nineteen public-domain translations work with no internet at all. Licensed translations fetch a verse at a time with the church&rsquo;s own key.", "The phone remote and the stage display run over the church&rsquo;s own Wi-Fi, with a PIN.", "No account, no analytics, no tracking. A sermon summary uses a language model only if the church adds its own key and asks for it."])}<p class="mt-16"><a class="btn ghost" href="/contact?topic=Lector">Ask about Lector</a></p></div>
    </div>
  </div>
</section>
'''
page("/lector", "Lector · The verse, the moment it is spoken", "Lector is a church presentation app for Mac that listens to the preacher and puts the scripture on the screens as it is read, then runs the rest of the service: songs, slides, videos, four screens, announcements, a stage display and a phone remote. Coming soon.", LECTOR, current="/lector", image="/img/photos/stage.jpg")

# ---------------------------------------------------------------- papersuite
PAPERSUITE = f'''
<section class="hero">
  <div class="photo" style="background-image:url(/img/photos/night.jpg)"></div><div class="bg" style="background:radial-gradient(900px 500px at 15% 10%,rgba(52,211,182,.22),transparent 60%),radial-gradient(700px 500px at 85% 20%,rgba(79,184,255,.16),transparent 60%)"></div>
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow-row"><img class="appicon" src="/img/kepta/icon.png" alt="PaperSuite app icon" width="64" height="64"><span class="pill"><span class="dot"></span>Coming soon</span><span class="pill">iPhone</span><span class="pill">Free</span></div>
      <h1>Every document, <span class="accent" style="background:linear-gradient(90deg,#34D3B6,#4FB8FF);-webkit-background-clip:text;background-clip:text">in one place.</span></h1>
      <p class="lead mt-24">Write the note. Scan the page, fill in the form, sign the PDF, and ask your own notes what you said last month. Keep your habits and streaks beside it all. PaperSuite holds every document in one place, and keeps it on your phone.</p>
      <div class="cta"><a class="btn primary" href="/contact?topic=PaperSuite">Tell me when it launches {I["arrow"]}</a><a class="btn ghost" href="#features">What it does</a></div>
    </div>
    <div class="phones"><div class="glow" style="background:radial-gradient(closest-side,rgba(52,211,182,.35),transparent)"></div>
      <div class="phone back"><img src="/img/kepta/habits.png" alt="PaperSuite habits grid with streaks and challenges" loading="eager"></div>
      <div class="phone front"><img src="/img/kepta/today.png" alt="PaperSuite Today screen: the week, the summary ring and today&rsquo;s habits" loading="eager"></div>
    </div>
  </div>
</section>

<section class="section" id="features">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Notes, documents and habits</span><h2 class="mt-8">Write it, scan it, sign it.</h2></div>
    <div class="grid g3">
      {feature("check", "Habits and streaks", "Daily habits, counted targets and 7, 30, 60 or 90-day challenges. Streaks walk the days you actually scheduled, so a weekday habit does not break every weekend.")}
      {feature("calendar", "A calendar that tells the truth", "Past days show what you logged. Future days show only what you put on them. Jump to any date from Today.")}
      {feature("type", "Notes, in plain markdown", "Headings, checklists, links and photos. Folders come from the notes themselves, so there is never an empty one. Export any note as text or PDF.")}
    </div>
    <div class="grid g3 mt-24">
      {feature("camera", "Scan", "Apple&rsquo;s own document scanner &mdash; edges, perspective and all &mdash; plus image to PDF for the pages you already have.")}
      {feature("hand", "Sign", "Open a PDF, draw your signature once, drop it on the page in black or blue ink, and export it signed.")}
      {feature("lyrics", "Ask your notes", "Ask a question and get an answer drawn only from your own writing. When your notes do not know, it says so instead of making something up.")}
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="product card reveal">
      <div class="copy"><span class="eyebrow">Honestly</span><h2 class="mt-8" style="font-size:clamp(26px,3vw,38px)">A streak is not the point.</h2><p class="lead mt-16" style="font-size:17px">Most habit apps stop at the tick, and a row of ticks says nothing about why a habit is sticking or slipping. PaperSuite keeps the note beside the habit &mdash; what you tried, what worked &mdash; and measures the week rather than the day, because one day is only ever 0, 50 or 100 percent. The number it shows you is the one that means something.</p></div>
      <div class="shots"><div class="phone"><img src="/img/kepta/calendar.png" alt="PaperSuite monthly calendar and streak board" loading="lazy"></div><div class="phone"><img src="/img/kepta/today.png" alt="PaperSuite Today" loading="lazy"></div></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="card reveal" style="display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:start"><div class="icon" style="margin:0">{I["shield"]}</div>
      <div><h3>Yours, on your phone.</h3>{check_list(["No account to create and nothing to sign in to. Your habits and notes live on the device.", "No advertising, no analytics, no tracking software of any kind.", "Scans and signatures are made on the phone and shared only when you choose to share them.", "Questions you ask your notes are answered by a language model and not stored there; nothing else ever leaves the device."])}<p class="mt-16"><a class="btn ghost" href="/contact?topic=PaperSuite">Ask about PaperSuite</a></p></div>
    </div>
  </div>
</section>
'''
page("/papersuite", "PaperSuite · Every document, in one place", "PaperSuite is an iPhone app for everything on paper: notes with photos and reminders, document scanning, filling in, signing, merging and converting PDFs, questions answered from your own notes, and habits with streaks. Coming soon.", PAPERSUITE, current="/papersuite", image="/img/photos/night.jpg")

# ---------------------------------------------------------------- kilojo
KILOJO = f'''
<section class="hero">
  <div class="photo" style="background-image:url(/img/photos/night.jpg)"></div><div class="bg" style="background:radial-gradient(900px 500px at 15% 10%,rgba(46,213,115,.22),transparent 60%),radial-gradient(700px 500px at 90% 30%,rgba(31,209,178,.22),transparent 60%)"></div>
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow-row"><span class="pill"><span class="dot"></span>Coming soon</span><span class="pill">iPhone</span><span class="pill">Free</span></div>
      <h1>A food diary that <span class="accent" style="background:var(--grad-cool);-webkit-background-clip:text;background-clip:text">reads your plate.</span></h1>
      <p class="lead mt-24">Photograph a meal and Kilojo estimates the calories and macronutrients. Scan a barcode and it takes the figures straight off the packet. Everything it produces is editable, because an estimate you cannot correct is a guess you are stuck with.</p>
      <div class="cta"><a class="btn green" href="/contact?topic=Kilojo">Ask about Kilojo {I["arrow"]}</a><a class="btn ghost" href="/kilojo/privacy">How your data is handled</a></div>
    </div>
    <div class="phones"><div class="glow" style="background:radial-gradient(closest-side,rgba(46,213,115,.35),transparent)"></div>
      <div class="phone back"><img src="/img/kilojo/3-progress.png" alt="Kilojo progress screen" loading="eager"></div>
      <div class="phone front"><img src="/img/kilojo/2-snap-your-meal.png" alt="Kilojo photographing a meal" loading="eager"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow green">Three ways in, and a plan</span><h2 class="mt-8">Photograph it, scan it, say it &mdash; or plan the week.</h2></div>
    <div class="grid g3">
      {feature("camera", "Point at the plate", "For food that never had a label: a plate of rice, a takeaway, someone else&rsquo;s cooking. Kilojo itemises what it can see and shows its working, so you can see why a number came out as it did.")}
      {feature("barcode", "Read the packet", "A barcode gives the manufacturer&rsquo;s own figures, which beats any estimate from a photograph. Instant, and free to run.")}
      {feature("type", "Or just say it", "Sometimes you know. Type the name and the numbers, and log a repeat of it in one tap for as long as you keep eating it.")}
    </div>
    <div class="grid g3 mt-24">
      {feature("calendar", "Plan the week", "Seven days, four slots each. Pick from meals you have logged or a cookbook of 216 everyday ones, or let Kilojo fill the empty slots to your target and edit what it picked.")}
      {feature("leaf", "Your way of eating", "Vegetarian, vegan, pescatarian, gluten-free, dairy-free, keto, high-protein or low-carb &mdash; every filter has real options for every meal of the day.")}
      {feature("scale", "Where you are heading", "A goal weight with the distance still to go, BMI on the WHO scale for context, and a weight trend that reads the line, not any one morning.")}
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="product card reveal">
      <div class="copy"><span class="eyebrow green">Honestly</span><h2 class="mt-8" style="font-size:clamp(26px,3vw,38px)">What a photograph cannot tell you.</h2><p class="lead mt-16" style="font-size:17px">A picture does not contain the portion. A bowl of rice can hold twice what it appears to, and no amount of cleverness recovers information the camera never captured. Kilojo estimates, and sometimes it is wrong.</p><p class="mt-16 dim">So it is built to be corrected: every figure is editable, it says how confident it is, and it shows the portion it assumed for each item rather than handing down a total. Tell it &ldquo;one cup of rice&rdquo; and the guess becomes arithmetic. Kilojo counts. It is not medical advice, and it does not have an opinion about your dinner.</p></div>
      <div class="shots"><div class="phone"><img src="/img/kilojo/1-today.png" alt="Kilojo today screen" loading="lazy"></div><div class="phone"><img src="/img/kilojo/3-progress.png" alt="Kilojo progress" loading="lazy"></div></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="card reveal" style="display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:start"><div class="icon" style="margin:0">{I["shield"]}</div>
      <div><h3>Your diary is yours.</h3>{check_list(["No advertising, no analytics, no tracking software of any kind.", "Meal photographs are sent for analysis carrying the picture and your typed hint, not your name or email.", "Barcode lookups send the number on the packet and nothing more.", "Erase everything, or delete the account outright, from inside the app. Both reach the server, not just the phone."])}<p class="mt-24"><a class="btn ghost" href="/kilojo/privacy">Privacy policy</a> &nbsp; <a class="btn ghost" href="/kilojo/terms">Terms of use</a></p></div>
    </div>
  </div>
</section>
'''
page("/kilojo", "Kilojo · A food diary that reads your plate", "Kilojo photographs a meal and estimates calories and macros, scans barcodes for the packet's own figures, and keeps every number editable. Coming soon for iPhone.", KILOJO, current="/kilojo", image="/img/photos/night.jpg")

# ---------------------------------------------------------------- work
WORK = f'''
<section class="hero" style="padding-bottom:20px">
  <div class="bg"></div>
  <div class="wrap"><span class="eyebrow">Work</span><h1 class="mt-16">Everything we are shipping.</h1><p class="lead mt-24">The list is short because it is honest. An app appears here once it is real and in testers&rsquo; hands, and it is marked released only once it is on the App Store.</p></div>
</section>
<section class="section">
  <div class="wrap grid g2">
    <a class="card product-card reveal" href="/gigpal"><div class="media"><img src="/img/photos/stage.jpg" alt="" loading="lazy"><img class="shot" src="/img/gigpal/chords.png" alt=""></div><div class="body"><span class="pill"><span class="dot"></span>On the App Store</span><h3 class="mt-16">GigPal</h3><p>Music practice: stems, chords, key and tempo, metronome, tuner, piano, recorder, setlists.</p><span class="btn primary">View GigPal {I["arrow"]}</span></div></a>
    <a class="card product-card reveal" href="/kilojo"><div class="media"><img src="/img/photos/night.jpg" alt="" loading="lazy"><img class="shot" src="/img/kilojo/1-today.png" alt=""></div><div class="body"><span class="pill"><span class="dot"></span>Coming soon</span><h3 class="mt-16">Kilojo</h3><p>A food diary that reads your plate: photo estimates, barcode scanning, editable numbers.</p><span class="btn green">View Kilojo {I["arrow"]}</span></div></a>
    <a class="card product-card reveal" href="/papersuite"><div class="media"><img src="/img/photos/night.jpg" alt="" loading="lazy"><img class="shot" src="/img/kepta/habits.png" alt=""></div><div class="body"><span class="pill"><span class="dot"></span>Coming soon</span><h3 class="mt-16">PaperSuite</h3><p>Notes, scans and PDFs in one app: fill in, sign, merge and convert documents, with habits and streaks beside them.</p><span class="btn primary">View PaperSuite {I["arrow"]}</span></div></a>
    <a class="card product-card reveal" href="/lector"><div class="media"><img src="/img/photos/stage.jpg" alt="" loading="lazy"><img class="shot wide" src="/img/lector/screen.png" alt=""></div><div class="body"><span class="pill"><span class="dot"></span>Coming soon</span><h3 class="mt-16">Lector</h3><p>Church presentation for Mac that hears the preacher and puts the verse on screen as it is spoken; songs, slides, videos, four screens and a stage display for the rest.</p><span class="btn primary">View Lector {I["arrow"]}</span></div></a>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Client work</span><h2 class="mt-8">How a project runs.</h2><p class="lead">Client work is not listed publicly unless the client wants it to be. What is worth saying is how it goes.</p></div>
    <div class="grid g4 steps">
      <div class="step reveal"><h3>Scope, written down</h3><p class="mt-8 dim">Screens, states and what is explicitly out. A fixed price against that document, so the number does not move unless the scope does.</p></div>
      <div class="step reveal"><h3>A build you can hold</h3><p class="mt-8 dim">Every week, installed on your own device rather than a screenshot in a deck. You see it going wrong early enough to say so.</p></div>
      <div class="step reveal"><h3>Submission included</h3><p class="mt-8 dim">App Store listing, privacy labels, review responses. The job is not done when the code is done.</p></div>
      <div class="step reveal"><h3>You own all of it</h3><p class="mt-8 dim">Repository, accounts, signing, the lot, documented well enough that another developer could pick it up without ringing us.</p></div>
    </div>
    <p class="mt-40 reveal"><a class="btn primary" href="/contact?topic=New%20project">Start a project {I["arrow"]}</a></p>
  </div>
</section>
'''
page("/work", "Work", "The apps Avodahsoft is shipping, and how client projects run: fixed scope, weekly builds, submission included, full handover.", WORK, current="/work")

# ---------------------------------------------------------------- studio
STUDIO = f'''
<section class="hero" style="padding-bottom:20px">
  <div class="photo" style="background-image:url(/img/photos/dev1.jpg)"></div><div class="bg"></div>
  <div class="wrap hero-grid">
    <div><span class="eyebrow">Studio</span><h1 class="mt-16">Work, service, worship. <span class="accent">One word.</span></h1><p class="lead mt-24">Avodah is the Hebrew word for work. It is also the word for service, and for worship. Ancient Hebrew did not split them into separate ideas: the same word covered the craftsman at his bench and the offering he made. That distinction never made much sense here either.</p></div>
    <div class="hero-photo-card reveal"><img src="/img/photos/dev2.jpg" alt="A developer working at a desk" loading="eager"><span class="tag pill">Founder-led · Australia</span></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">The name</span><h2 class="mt-8">Care is the whole point.</h2><p class="lead">Work done carefully is worth something on its own terms, whoever is watching and whether or not anyone notices the part that took the longest. It is why nothing ships half-finished, why the code is written to be read by whoever comes next, and why one honest estimate beats winning a job on an optimistic one.</p></div>
    <div class="grid g2">
      {feature("mail", "You talk to the person building it", "No account manager relaying your question to someone who has not read the code. The studio is small on purpose and stays that way.")}
      {feature("build", "Scope in writing, price fixed to it", "Screens, states and what is deliberately excluded. The number moves only when the document does, and then you decide.")}
      {feature("ship", "Working software every week", "On your device, not in a slide. The point is that you can tell us it is wrong while it is still cheap to change.")}
      {feature("hand", "Everything handed over", "Repository, accounts, signing keys and notes explaining the decisions, so you are never held hostage by the only person who understands it.")}
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="band reveal"><img src="/img/photos/studio2.jpg" alt="A recording studio" loading="lazy">
      <div><span class="eyebrow">Fit</span><h3 class="mt-8">Who this suits.</h3><p>Founders and small teams with a clear idea and a real user in mind, who would rather have one considered thing than five rushed ones. Less good for projects that need twenty people by Friday, or for anyone wanting a body to fill a seat on an existing team.</p><a class="btn primary mt-24" href="/contact">Get in touch {I["arrow"]}</a></div>
    </div>
  </div>
</section>
'''
page("/studio", "Studio", "Avodahsoft is a founder-led software studio in Australia. Work, service and worship are one word, and care is the whole point.", STUDIO, current="/studio", image="/img/photos/dev2.jpg")

# ---------------------------------------------------------------- contact
CONTACT = f'''
<section class="hero" style="padding-bottom:20px">
  <div class="bg"></div>
  <div class="wrap"><span class="eyebrow">Contact</span><h1 class="mt-16">What brings you here?</h1><p class="lead mt-24">Everything reaches the same inbox. Picking the closest topic just means a faster and more useful answer. Support gets answered first, usually the same day.</p></div>
</section>
<section class="section">
  <div class="wrap grid g2" style="align-items:start">
    <div class="card reveal">
      <form class="form" data-contact novalidate>
        <div class="row"><input name="name" placeholder="Your name" autocomplete="name" required minlength="2"><input name="email" type="email" placeholder="Email address" autocomplete="email" required></div>
        <select name="topic" id="topic"><option>Support · GigPal</option><option>Support · Kilojo</option><option>GigPal early access</option><option>Kilojo</option><option>PaperSuite</option><option>Lector</option><option>New project</option><option>Acquisition</option><option>Other</option></select>
        <textarea name="message" placeholder="Say which app and which phone if it is support. For a project, the idea, who it is for and roughly when it needs to be live." required minlength="10"></textarea>
        <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap"><button class="btn primary" type="submit">Send message {I["arrow"]}</button><span class="status" role="status"></span></div>
        <p class="small dim">Or email <a href="mailto:{MAIL}" style="color:var(--orange-2)">{MAIL}</a> directly. Messages are sent to the studio and used only to reply to you.</p>
      </form>
    </div>
    <div class="stack">
      {feature("mail", "I use one of your apps", "Something is broken, a question about your account, or a feature you wish existed. Say which app and which phone, and we will sort it.")}
      {feature("build", "I want an app built", "The idea, who it is for, and roughly when it needs to be live. A budget range saves us both a round trip. If it is not a fit we will say so and, where we can, point you somewhere better.")}
      {feature("hand", "I am interested in buying", "Enquiries about acquiring one of our apps, in whole or in part, are welcome. You will get a real reply rather than a calendar link.")}
    </div>
  </div>
</section>
<script>try{{var t=new URLSearchParams(location.search).get('topic');if(t){{var s=document.getElementById('topic');for(var o of s.options)if(o.text.toLowerCase().indexOf(t.toLowerCase())>-1){{s.value=o.text;break}}}}}}catch(e){{}}</script>
'''
page("/contact", "Contact", "Support for GigPal and Kilojo, new project enquiries and acquisitions. Everything reaches the same inbox and gets a real reply.", CONTACT, current="/contact")

# ---------------------------------------------------------------- legal helpers
def legal_page(path, app, kind, intro, body_html, image):
    title = f"{app} {'privacy policy' if kind == 'privacy' else 'terms of use'}"
    other = ("terms", "Terms of use") if kind == "privacy" else ("privacy", "Privacy policy")
    body = f'''
<section class="hero" style="padding-bottom:0"><div class="bg"></div>
  <div class="wrap"><span class="eyebrow">{app} · Legal</span><h1 class="mt-16" style="font-size:clamp(32px,4.5vw,56px)">{'Privacy policy' if kind == 'privacy' else 'Terms of use'}</h1><p class="lead mt-24">{intro}</p>
  <p class="mt-24"><a class="pill" href="/{app.lower()}/{other[0]}">{other[1]} {I["arrow"]}</a> &nbsp; <a class="pill" href="/{app.lower()}">About {app}</a></p></div>
</section>
<section class="section" style="padding-top:40px"><div class="wrap"><div class="prose">{body_html}</div></div></section>'''
    page(path, title, intro, body, current=f"/{app.lower()}", image=image)


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
<p>GigPal is made and operated by Avodahsoft, an independent software studio based in Australia. You can reach us at <a href="mailto:{MAIL}">{MAIL}</a>. We are the data controller for the personal information described here.</p>

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
PAPERSUITE_UPDATED = "4 October 2026"

KP_PRIVACY = f'''
<p class="meta">Last updated {PAPERSUITE_UPDATED} &middot; PaperSuite for iPhone &middot; Operated by Avodahsoft, Australia</p>
<div class="callout"><b>In one paragraph.</b> PaperSuite works without an account, and your notes, PDFs, scans, signatures, photos, reminders and habits are kept on your iPhone. If you choose to sign in with Apple, the text of your notes and your habits are synced to your account so they are backed up and on your other devices; photos and PDFs stay on the phone. If you use Ask AI or the writing tools, the text needed for that request is sent to our server and to Anthropic to produce the answer, and is not kept. There is no advertising, no analytics and no tracking, and you can delete your account and everything synced with it from inside the app.</div>

<h2>Who we are</h2>
<p>PaperSuite is made and operated by Avodahsoft, an independent software studio based in Australia. You can reach us at <a href="mailto:{MAIL}">{MAIL}</a>. We are the data controller for the personal information described here.</p>

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
<p>These features are optional and part of PaperSuite Pro. When you use one, the text needed for that request is sent over HTTPS to our server and from there to Anthropic, whose Claude model writes the answer. That text is your question or instruction, the passage you selected, and, for questions about your notes, the notes most relevant to it. Locked notes and the pictures in your notes are never included. To count requests against your monthly allowance, our server records how many requests an identifier made each day; that identifier is a random one the app creates for you, or your account if you have signed in. We do not store the content of your requests or the answers. Anthropic processes them under its commercial terms, which do not allow it to train models on them, and keeps them only briefly for abuse monitoring.</p>
<p>AI answers can be wrong. PaperSuite never applies one to your notes by itself: it is shown to you first, and nothing changes until you choose.</p>

<h2>PaperSuite Pro and purchases</h2>
<p>PaperSuite Pro is an auto-renewing subscription sold through Apple. Apple processes the payment and we never see your card details. We use RevenueCat to confirm whether a subscription is active: it receives your purchase records from Apple and the app&rsquo;s random identifier, and tells our server whether Pro is active.</p>

<h2>App updates</h2>
<p>When it starts, PaperSuite checks Expo&rsquo;s update service for fixes and downloads them. The check includes the app&rsquo;s version and platform and, like any web request, your IP address. It contains no account details or note content. Updates are signed, and the app refuses one that is not.</p>

<h2>Device permissions</h2>
<ul>
  <li><b>Camera:</b> to scan documents and take photos, only when you choose to.</li>
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
<tr><td>Supabase</td><td>Accounts, sync and the server behind Ask AI</td><td>Account details, synced notes and habits, daily AI request counts</td></tr>
<tr><td>Anthropic</td><td>AI answers and writing help</td><td>The text of each request, briefly</td></tr>
<tr><td>Apple</td><td>Sign in with Apple, App Store distribution and payments</td><td>Handled under Apple&rsquo;s privacy policy</td></tr>
<tr><td>RevenueCat</td><td>Subscription status</td><td>Purchase records and a random identifier</td></tr>
<tr><td>Expo</td><td>App updates</td><td>App version and platform, IP address</td></tr>
<tr><td>Cloudflare</td><td>Hosting avodahsoft.com</td><td>Standard web request data; no app data</td></tr></table>
<p>These providers may process data in the United States, South Korea and other countries. We choose providers that commit to industry-standard security and data-protection terms.</p>

<h2>Retention and deletion</h2>
<p>Notes go to Recently Deleted and are removed after 30 days, or straight away if you empty it. You can delete your account from the Profile screen; this permanently removes your account and everything synced with it from our servers at once. Deleting your account does not cancel a PaperSuite Pro subscription: cancel it in your iPhone&rsquo;s Settings, under your name and Subscriptions. What is on the phone is removed when you delete the app; export your notes first if you want a copy. To ask for deletion or a copy of your data by email, write to <a href="mailto:{MAIL}">{MAIL}</a>.</p>

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
<section class="hero"><div class="bg"></div><div class="wrap center"><span class="eyebrow">404</span><h1 class="mt-16">That page is not here.</h1><p class="lead mt-24" style="margin-inline:auto">The link may be old. Try the home page, or write to us if you were looking for something specific.</p><p class="mt-24"><a class="btn primary" href="/">Go home {I["arrow"]}</a> &nbsp; <a class="btn ghost" href="/contact">Contact</a></p></div></section>'''
page("/404", "Page not found", "That page is not here.", NOTFOUND, out="/404.html")

write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
paths = ["/", "/gigpal", "/kilojo", "/papersuite", "/lector", "/work", "/studio", "/contact", "/gigpal/privacy", "/gigpal/terms", "/kilojo/privacy", "/kilojo/terms", "/papersuite/privacy", "/papersuite/terms"]
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{p}</loc></url>\n" for p in paths) + "</urlset>\n")
write("/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFB547"/><stop offset=".55" stop-color="#FF7A3D"/><stop offset="1" stop-color="#FF5E62"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="url(#g)"/><path d="M20 46 32 16l12 30h-6.6l-2.4-6.4H29l-2.4 6.4Zm10.6-12h6.8L34 24.6Z" fill="#0A0E1F"/></svg>')
print("done")
