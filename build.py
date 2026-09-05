#!/usr/bin/env python3
"""Generates the static pages in ./public. Run `python3 build.py`, then `npx wrangler deploy`."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).parent
PUB = ROOT / "public"
SITE = "https://avodahsoft.com"
MAIL = "hello@avodahsoft.com"
UPDATED = "6 September 2026"
YEAR = "2026"

I = {
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M20 6 9 17l-5-5"/></svg>',
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
    "camera": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M3 8a2 2 0 0 1 2-2h2l2-3h6l2 3h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8Z"/><circle cx="12" cy="13" r="4"/></svg>',
    "barcode": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="color:var(--teal)"><path d="M4 5v14M8 5v14M11 5v14M15 5v14M18 5v14M21 5v14"/></svg>',
    "type": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--purple)"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--green)"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "build": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--orange)"><path d="m14.7 6.3 3 3L7 20H4v-3L14.7 6.3Z"/><path d="m16 5 3 3"/></svg>',
    "ship": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--teal)"><path d="M5 18 3 12l9-3 9 3-2 6"/><path d="M12 9V3"/><path d="M2 21c2 0 3-1 5-1s3 1 5 1 3-1 5-1 3 1 5 1"/></svg>',
    "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--purple)"><path d="M12 3v12"/><path d="m8 11 4 4 4-4"/><path d="M4 17v3h16v-3"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--orange)"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
}

NAV = [("/gigpal", "GigPal"), ("/kilojo", "Kilojo"), ("/work", "Work"), ("/studio", "Studio"), ("/contact", "Contact")]


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
    <div><h4>Apps</h4><a href="/gigpal">GigPal</a><a href="/kilojo">Kilojo</a><a href="/work">All work</a></div>
    <div><h4>Studio</h4><a href="/studio">About</a><a href="/contact">Contact</a><a href="/contact?topic=Support">Support</a></div>
    <div><h4>Legal</h4><a href="/gigpal/privacy">GigPal privacy</a><a href="/gigpal/terms">GigPal terms</a><a href="/kilojo/privacy">Kilojo privacy</a><a href="/kilojo/terms">Kilojo terms</a></div>
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
    <div class="section-head reveal"><span class="eyebrow">Our apps</span><h2 class="mt-8">Two products, one standard.</h2><p class="lead">Each one is built by the person who answers your email, and each ships when it is genuinely finished.</p></div>
    <div class="grid g2">
      <a class="card product-card reveal" href="/gigpal">
        <div class="media"><img src="/img/photos/band.jpg" alt="A band rehearsing on stage" loading="lazy"><img class="shot" src="/img/gigpal/library.png" alt=""></div>
        <div class="body"><div class="eyebrow-row"><span class="pill"><span class="dot"></span>In development</span><span class="pill">iOS · iPad · Web</span></div><h3>GigPal</h3><p>The practice room in your pocket. Split any song into vocals, piano, bass, drums and more, follow the chords as they play, change key and tempo, and rehearse with a metronome, tuner and recorder.</p><span class="btn primary">Explore GigPal {I["arrow"]}</span></div>
      </a>
      <a class="card product-card reveal" href="/kilojo">
        <div class="media"><img src="/img/photos/night.jpg" alt="A table set for dinner in the evening" loading="lazy"><img class="shot" src="/img/kilojo/2-snap-your-meal.png" alt=""></div>
        <div class="body"><div class="eyebrow-row"><span class="pill"><span class="dot"></span>Coming soon</span><span class="pill">iOS</span></div><h3>Kilojo</h3><p>A food diary that reads your plate. Photograph a meal for calories and macros, scan a barcode for the packet&rsquo;s own figures, or simply type it in. Every number stays editable.</p><span class="btn green">Explore Kilojo {I["arrow"]}</span></div>
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
page("/", "Avodahsoft · Apps for musicians and everyday life", "Avodahsoft is an independent software studio in Australia building GigPal, the music practice app, and Kilojo, the food diary that reads your plate.", HOME)

# ---------------------------------------------------------------- gigpal
GIGPAL = f'''
<section class="hero">
  <div class="photo" style="background-image:url(/img/photos/concert.jpg)"></div><div class="bg"></div>
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow-row"><img class="appicon" src="/img/gigpal/icon.png" alt="GigPal app icon" width="64" height="64"><span class="pill"><span class="dot"></span>In development · App Store {YEAR}</span><span class="pill">iPhone · iPad · Web</span></div>
      <h1>Practice like <span class="accent">the band is in the room.</span></h1>
      <p class="lead mt-24">GigPal turns any song into a rehearsal. Pull the vocals, piano, bass and drums apart, follow the chords as they change, slow it down, move the key, loop the hard bit, and record yourself over the top.</p>
      <div class="cta"><a class="btn primary" href="/contact?topic=GigPal%20early%20access">Get early access {I["arrow"]}</a><a class="btn ghost" href="#features">See what it does</a></div>
      <div class="stats"><div><b>5</b>stems per song</div><div><b>3</b>chord notations</div><div><b>&plusmn;12</b>semitones of key change</div><div><b>0</b>ads or trackers</div></div>
    </div>
    <div class="phones"><div class="glow"></div>
      <div class="phone back"><img src="/img/gigpal/profile.png" alt="GigPal profile and settings" loading="eager"></div>
      <div class="phone front"><img src="/img/gigpal/chords.png" alt="GigPal chords following the song" loading="eager"></div>
    </div>
  </div>
</section>

<section class="section" id="features">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Everything a rehearsal needs</span><h2 class="mt-8">One app, the whole practice room.</h2><p class="lead">Built for gigging musicians, worship teams, choirs, students and anyone who learns songs by ear.</p></div>
    <div class="grid g3">
      {feature("layers", "Stem mixer", "Separate a song into vocals, piano and keys, bass, drums and everything else. Solo the part you are learning, mute the part you play, or split the vocals into lead and backing.")}
      {feature("chord", "Chords that follow the song", "The chord progression is detected on your device and highlighted bar by bar as the song plays. Read it as letters, as numbers (1, 4, 5, 7&flat;) or as solfa.")}
      {feature("gauge", "Key and tempo", "Every song is analysed for key, tempo and beats the moment you add it. Re-analyse in a tap if you disagree, and see it laid out on a piano.")}
      {feature("speed", "Speed and pitch", "Slow a passage to half speed without changing the pitch, or move the whole song into your singing key. Both stay locked to the chords and lyrics.")}
      {feature("loop", "Sections and loops", "GigPal finds the intro, verses and choruses. Tap a section to jump to it or loop it until it is under your fingers.")}
      {feature("lyrics", "Lyrics finder", "Pull in synced lyrics for the song you are working on, follow them as they scroll, and translate chord symbols in your own charts to numbers or solfa.")}
      {feature("metro", "Metronome", "A rock-solid metronome with tap tempo, count-in, accents and subdivisions, designed to be heard over a full band.")}
      {feature("tuner", "Tuner", "A chromatic tuner with a clear needle and cents readout. Works for voice, guitar, bass, brass and strings.")}
      {feature("piano", "Piano and solfa", "A sampled grand piano to check a note or find a starting pitch, plus a solfa trainer for singers who read do-re-mi.")}
      {feature("mic", "Recorder", "Record yourself over the mix or on its own. Every take is analysed for key and tempo too, so you can see how the rehearsal went.")}
      {feature("list", "Setlists", "Group songs into setlists for a gig or a service, reorder them by drag, and move through the set without leaving the player.")}
      {feature("bell", "Reminders and links", "Set practice reminders, and add songs from your files, camera roll, a direct link, or play along with YouTube, Spotify and Apple Music.")}
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
      <div class="step reveal"><h3>Separate the stems</h3><p class="mt-8 dim">With GigPal Pro, the song is separated in the cloud using the same open-source model family the big apps rely on, then deleted from our servers.</p></div>
      <div class="step reveal"><h3>Practise</h3><p class="mt-8 dim">Mix the parts, follow the chords, slow it down, loop it, record yourself. Then add it to the setlist for Sunday.</p></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grid g2" style="align-items:start">
      <div class="reveal"><span class="eyebrow">Free and Pro</span><h2 class="mt-8">Most of GigPal is free. Stems are Pro.</h2><p class="lead mt-16">Everything that runs on your phone stays free forever. Cloud stem separation costs real computing time, so it lives in a GigPal Pro subscription billed through the App Store. Pricing will be announced at launch and you can cancel any time in your Apple settings.</p></div>
      <div class="card reveal" style="padding:10px 18px">
        <table class="compare">
          <tr><th>Feature</th><th>Free</th><th>Pro</th></tr>
          <tr><td>Library, key, tempo, chords, sections</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
          <tr><td>Speed and pitch, loops, lyrics</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
          <tr><td>Metronome, tuner, piano, solfa, recorder</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
          <tr><td>Setlists, reminders, sync across devices</td><td class="yes">&check;</td><td class="yes">&check;</td></tr>
          <tr><td>Stem separation (vocals, piano, bass, drums, other)</td><td class="no">&ndash;</td><td class="yes">&check;</td></tr>
          <tr><td>Lead and backing vocal split</td><td class="no">&ndash;</td><td class="yes">&check;</td></tr>
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
    <div class="section-head reveal"><span class="eyebrow green">Three ways in</span><h2 class="mt-8">Photograph it, scan it, or just say it.</h2></div>
    <div class="grid g3">
      {feature("camera", "Point at the plate", "For food that never had a label: a plate of rice, a takeaway, someone else&rsquo;s cooking. Kilojo itemises what it can see and shows its working, so you can see why a number came out as it did.")}
      {feature("barcode", "Read the packet", "A barcode gives the manufacturer&rsquo;s own figures, which beats any estimate from a photograph. Instant, and free to run.")}
      {feature("type", "Or just say it", "Sometimes you know. Type the name and the numbers, and log a repeat of it in one tap for as long as you keep eating it.")}
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
    <a class="card product-card reveal" href="/gigpal"><div class="media"><img src="/img/photos/stage.jpg" alt="" loading="lazy"><img class="shot" src="/img/gigpal/chords.png" alt=""></div><div class="body"><span class="pill"><span class="dot"></span>In development</span><h3 class="mt-16">GigPal</h3><p>Music practice: stems, chords, key and tempo, metronome, tuner, piano, recorder, setlists.</p><span class="btn primary">View GigPal {I["arrow"]}</span></div></a>
    <a class="card product-card reveal" href="/kilojo"><div class="media"><img src="/img/photos/night.jpg" alt="" loading="lazy"><img class="shot" src="/img/kilojo/1-today.png" alt=""></div><div class="body"><span class="pill"><span class="dot"></span>Coming soon</span><h3 class="mt-16">Kilojo</h3><p>A food diary that reads your plate: photo estimates, barcode scanning, editable numbers.</p><span class="btn green">View Kilojo {I["arrow"]}</span></div></a>
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
        <select name="topic" id="topic"><option>Support · GigPal</option><option>Support · Kilojo</option><option>GigPal early access</option><option>Kilojo</option><option>New project</option><option>Acquisition</option><option>Other</option></select>
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
<p>Your library lives on your device: the songs and recordings you add, the analysis results (key, tempo, beats, chords, sections and lyrics timing), any separated stems, your setlists, reminders and settings. This information stays on the device unless you sign in and turn on sync, or unless you choose to share something. Deleting a song in the app deletes it and its stems from the device.</p>

<h2>Information we collect when you sign in</h2>
<p>An account is optional. Without one, GigPal does not send us any personal information. If you create an account (by email and password) we store:</p>
<ul>
  <li><b>Account details:</b> your email address, a random account identifier, and the dates you signed up and last signed in.</li>
  <li><b>Library metadata for sync:</b> song titles, artists, keys, tempos, chord and section data, setlists, reminders and preferences, so your library can be restored on another device. Audio files and recordings are not uploaded for sync.</li>
  <li><b>Separation history:</b> the time, duration and size of each stem separation job, used to apply fair-use limits and to bill Pro subscriptions correctly. We do not keep the audio.</li>
</ul>
<p>Accounts and synced data are hosted on Supabase infrastructure, protected by per-user access rules so that one account can never read another&rsquo;s data.</p>

<h2>Stem separation</h2>
<p>When you ask GigPal to separate a song, the audio file is uploaded over HTTPS to our separation service, processed with an open-source source-separation model (Demucs), and the resulting stems are returned to your device. The uploaded audio and the generated stems are deleted from our servers automatically once your device has downloaded them, and in any case within 24 hours. We do not listen to, analyse for other purposes, or train models on your audio. Stem separation requires a signed-in account so that we can apply limits and subscriptions.</p>

<h2>Third-party lookups you trigger</h2>
<ul>
  <li><b>Lyrics.</b> When you search for lyrics, the song title and artist you provide are sent to LRCLIB (lrclib.net), an open lyrics database. No account information is included.</li>
  <li><b>Rhymes.</b> In the lyric writer, the word you look up is sent to the Datamuse API to fetch rhymes and related words.</li>
  <li><b>Play-along links.</b> If you paste a YouTube, Spotify or Apple Music link, the content is played inside an embedded player provided by that service. Those services may set cookies or collect data under their own privacy policies. GigPal does not download or store that content.</li>
</ul>

<h2>Device permissions</h2>
<ul>
  <li><b>Microphone</b> is used only while the tuner, live chords or recorder screens are open. Audio from the microphone is processed on the device and is not sent anywhere unless you explicitly separate or share a recording you made.</li>
  <li><b>Photo library and files</b> are accessed only when you choose a video or audio file to import, and only for the item you pick.</li>
  <li><b>Notifications</b> are used for practice reminders you set. They are scheduled on the device; we do not operate a push-notification server.</li>
</ul>

<h2>Purchases</h2>
<p>GigPal Pro is sold as an in-app subscription through Apple. Apple processes the payment and we never see your card details. We receive an anonymous subscription status (via RevenueCat) so that the app can unlock Pro features on your devices. Manage or cancel the subscription in your Apple ID settings.</p>

<h2>What we do not do</h2>
<ul>
  <li>No advertising, no advertising identifiers.</li>
  <li>No analytics or tracking SDKs. We do not track you across apps or websites.</li>
  <li>No selling, renting or sharing of personal information with data brokers.</li>
</ul>

<h2>Service providers</h2>
<table><tr><th>Provider</th><th>Purpose</th><th>Data involved</th></tr>
<tr><td>Supabase</td><td>Accounts, database and file storage</td><td>Email, account id, synced library metadata</td></tr>
<tr><td>Our separation service (Fly.io hosting)</td><td>Stem separation</td><td>Uploaded audio, temporarily</td></tr>
<tr><td>Apple</td><td>App distribution and in-app purchases</td><td>Handled under Apple&rsquo;s privacy policy</td></tr>
<tr><td>RevenueCat</td><td>Subscription status</td><td>Anonymous app user id, purchase receipt</td></tr>
<tr><td>Resend</td><td>Account emails (password resets)</td><td>Email address</td></tr>
<tr><td>LRCLIB, Datamuse</td><td>Lyrics and rhyme lookups</td><td>Search terms only</td></tr></table>
<p>These providers may process data in the United States and other countries. We choose providers that commit to industry-standard security and data-protection terms.</p>

<h2>Retention and deletion</h2>
<p>You can delete songs, recordings and stems at any time on the device. You can delete your account from the Profile screen inside the app; this removes your account, synced library data and separation history from our servers, normally immediately and in all cases within 30 days. Uploaded audio for separation is deleted within 24 hours as described above. If you would rather email us to request deletion or a copy of your data, write to <a href="mailto:{MAIL}">{MAIL}</a>.</p>

<h2>Security</h2>
<p>All traffic between the app and our services is encrypted with HTTPS. Sign-in tokens are stored in the device&rsquo;s secure keychain. Database access is restricted with row-level security so that requests are always scoped to the signed-in account. No system is perfectly secure, and we will notify affected users if we become aware of a breach involving their personal information.</p>

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
<p>GigPal is a practice tool for musicians. It analyses songs you add for key, tempo, chords and structure, lets you change speed and pitch, provides a metronome, tuner, piano, recorder, lyrics tools and setlists, and, with a Pro subscription, separates songs into stems in the cloud.</p>

<h2>Your music and your responsibility</h2>
<ul>
  <li>You keep all rights to the recordings, songs and other content you add to GigPal. We only use them to provide the service to you.</li>
  <li>You must only import, upload or separate music that you own or have permission to use for this purpose: your own recordings and demos, tracks you have lawfully acquired for personal practice, and material released under licences that allow it. You are responsible for complying with copyright law in your country.</li>
  <li>Stems and other outputs are for your personal practice, study and performance preparation. Do not redistribute, sell or publish separated stems of music you do not own the rights to.</li>
  <li>We may suspend or terminate accounts that misuse the service, including abusive volumes of uploads or clear copyright infringement.</li>
</ul>

<h2>Accounts</h2>
<p>An account is optional for most of GigPal and required for sync and stem separation. Keep your credentials private; you are responsible for activity under your account. You can delete your account at any time from the Profile screen.</p>

<h2>GigPal Pro and payments</h2>
<ul>
  <li>GigPal Pro is an auto-renewing subscription purchased through Apple&rsquo;s App Store. Prices are shown in the app before you buy and may vary by country.</li>
  <li>The subscription renews automatically unless you cancel at least 24 hours before the end of the current period. Manage or cancel it in your Apple ID settings; deleting the app does not cancel a subscription.</li>
  <li>Refunds are handled by Apple under its policies. Your statutory rights are not affected.</li>
  <li>Stem separation is subject to fair-use limits shown in the app (for example a number of songs per day or per month) so that the service stays fast for everyone. We may adjust limits, features and prices over time, and will tell you in the app before a price change applies to you.</li>
</ul>

<h2>Acceptable use</h2>
<p>Do not attempt to reverse engineer, bypass limits, disrupt or overload the service, access another user&rsquo;s data, or use GigPal for anything unlawful. Automated or bulk use of the separation service is not permitted without our written agreement.</p>

<h2>Third-party services</h2>
<p>GigPal can open YouTube, Spotify and Apple Music content in embedded players and look up lyrics and rhymes from third-party databases. Those services are governed by their own terms, and we do not control their availability or content. GigPal does not download or store third-party streamed content.</p>

<h2>Accuracy and safety</h2>
<ul>
  <li>Detected keys, tempos, chords, sections and tuner readings are estimates produced by signal analysis. They are usually right and sometimes wrong. Check them with your ears before you rely on them in a performance.</li>
  <li>Protect your hearing: keep playback and headphone volumes at safe levels, especially when using the metronome or looping loud passages.</li>
</ul>

<h2>Availability and changes</h2>
<p>We aim to keep the cloud services running but cannot promise uninterrupted availability. We may change, suspend or discontinue features, and we may update these terms. When a change is significant we will tell you in the app; continuing to use GigPal after that means you accept the updated terms.</p>

<h2>Disclaimer and liability</h2>
<p>GigPal is provided &ldquo;as is&rdquo; to the extent permitted by law. Nothing in these terms excludes rights you have under the Australian Consumer Law or any other consumer protection law that cannot be excluded. Subject to those rights, we are not liable for indirect or consequential loss, and our total liability to you in connection with GigPal is limited to the amount you paid us for the service in the 12 months before the claim arose.</p>

<h2>Termination</h2>
<p>You can stop using GigPal and delete your account at any time. We may suspend or close accounts that breach these terms. On termination your right to use Pro features ends; content stored on your device remains yours.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of Australia, without limiting any mandatory consumer protection you have where you live.</p>
<p><b>Contact:</b> <a href="mailto:{MAIL}">{MAIL}</a></p>
'''
legal_page("/gigpal/terms", "GigPal", "terms", "The short version: your music stays yours, only add music you have the right to use, and stem separation is a Pro subscription billed by Apple that you can cancel any time.", GP_TERMS, "/img/photos/concert.jpg")

# ---------------------------------------------------------------- 404, robots, sitemap, favicon
NOTFOUND = f'''
<section class="hero"><div class="bg"></div><div class="wrap center"><span class="eyebrow">404</span><h1 class="mt-16">That page is not here.</h1><p class="lead mt-24" style="margin-inline:auto">The link may be old. Try the home page, or write to us if you were looking for something specific.</p><p class="mt-24"><a class="btn primary" href="/">Go home {I["arrow"]}</a> &nbsp; <a class="btn ghost" href="/contact">Contact</a></p></div></section>'''
page("/404", "Page not found", "That page is not here.", NOTFOUND, out="/404.html")

write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
paths = ["/", "/gigpal", "/kilojo", "/work", "/studio", "/contact", "/gigpal/privacy", "/gigpal/terms", "/kilojo/privacy", "/kilojo/terms"]
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{p}</loc></url>\n" for p in paths) + "</urlset>\n")
write("/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFB547"/><stop offset=".55" stop-color="#FF7A3D"/><stop offset="1" stop-color="#FF5E62"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="url(#g)"/><path d="M20 46 32 16l12 30h-6.6l-2.4-6.4H29l-2.4 6.4Zm10.6-12h6.8L34 24.6Z" fill="#0A0E1F"/></svg>')
print("done")
