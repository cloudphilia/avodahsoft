#!/usr/bin/env python3
"""Emits the site. No framework, no build step at deploy time — this runs once,
by hand, and the HTML it writes is what GitHub Pages serves."""
import io, re

MAIL = "hello@avodahsoft.com"

def head(title, desc, page):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>

<header class="bar">
  <div class="wrap">
    <a class="wordmark" href="index.html">Avodah <span lang="he" dir="rtl">עֲבוֹדָה</span></a>
    <nav class="nav">
      <a href="work.html"{cur(page,'work')}>Work</a>
      <a href="studio.html"{cur(page,'studio')}>Studio</a>
      <a href="contact.html"{cur(page,'contact')}>Contact</a>
    </nav>
  </div>
</header>

<main>'''

def cur(page, name):
    return ' aria-current="page"' if page == name else ''

FOOT = f'''</main>

<footer class="foot">
  <div class="wrap">
    <div class="stack-sm">
      <div class="wordmark">Avodah <span lang="he" dir="rtl">עֲבוֹדָה</span></div>
      <p class="small dim">Software studio. <a class="ln" href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
    <div class="foot-links">
      <a href="work.html">Work</a>
      <a href="studio.html">Studio</a>
      <a href="contact.html">Contact</a>
      <a href="legal.html#privacy">Privacy</a>
      <a href="legal.html#terms">Terms</a>
    </div>
  </div>
</footer>

<script>
(function () {{
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var items = document.querySelectorAll(".rv");
  if (reduce || !("IntersectionObserver" in window)) {{
    items.forEach(function (el) {{ el.classList.add("in"); }});
    return;
  }}
  var io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (e) {{
      if (!e.isIntersecting) return;
      var sibs = Array.prototype.filter.call(e.target.parentNode.children, function (n) {{
        return n.classList.contains("rv");
      }});
      e.target.style.transitionDelay = Math.max(0, sibs.indexOf(e.target)) * 55 + "ms";
      e.target.classList.add("in");
      io.unobserve(e.target);
    }});
  }}, {{ threshold: .12, rootMargin: "0px 0px -6% 0px" }});
  items.forEach(function (el) {{ io.observe(el); }});
}})();
</script>
</body>
</html>
'''

def write(name, title, desc, page, body):
    io.open(name, "w", encoding="utf-8").write(head(title, desc, page) + body + FOOT)
    print("wrote", name)

# ------------------------------------------------------------------ home ----
write("index.html", "Avodah — Software Studio",
      "A small software studio building iOS and web products, and client work made properly.",
      "home", f'''
<section class="hero flush">
  <div class="wrap">
    <p class="label label--accent">Software studio</p>
    <h1 style="margin-top:20px">A small studio that finishes things.</h1>
    <p class="lede">We design and build software for iOS and the web — our own products,
      released under our own name, and client work for people who want it made properly
      rather than quickly.</p>
    <div class="actions">
      <a class="btn btn--fill" href="work.html">See the work <span class="arw">&rarr;</span></a>
      <a class="btn" href="contact.html">Start a project <span class="arw">&rarr;</span></a>
    </div>
    <div class="meta">
      <div><span class="label">Founded</span><b>2026</b></div>
      <div><span class="label">Platforms</span><b>iOS &middot; Web</b></div>
      <div><span class="label">Team</span><b>Founder-led</b></div>
      <div><span class="label">Availability</span><b>Taking work</b></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">Selected work</p>
    <div class="stack">
      <div class="ledger">
        <a class="entry rv" href="kilojo.html">
          <span class="n">01</span>
          <h3>Kilojo</h3>
          <p class="small dim">Photograph a meal and get the calories and macros back in
            seconds. Barcode scanning reads the packet&rsquo;s own label.</p>
          <span class="state">Coming soon</span>
        </a>
      </div>
      <p class="small dim">One entry, because an app appears here when it is on the App Store
        and not before. <a class="ln" href="work.html">More about the work &rarr;</a></p>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">What we do</p>
    <div class="grid grid-3">
      <div class="cell rv">
        <p class="label label--accent">01 &mdash; Build</p>
        <h3>We build your app</h3>
        <p class="small dim">You have the idea and know the market. We handle design,
          development, App Store submission and the first release. Fixed scope, fixed price,
          something working in your hands every week.</p>
      </div>
      <div class="cell rv">
        <p class="label label--accent">02 &mdash; Ship</p>
        <h3>We run our own</h3>
        <p class="small dim">Products released under the studio&rsquo;s name and supported by
          the person who wrote them. No ticket queue &mdash; you email the studio, the studio
          answers.</p>
      </div>
      <div class="cell rv">
        <p class="label label--accent">03 &mdash; Hand over</p>
        <h3>We sell them properly</h3>
        <p class="small dim">Where an app finds the right owner: clean codebase, documented
          handover, whatever revenue history exists, and a transition long enough that
          nothing breaks on your watch.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">Approach</p>
    <div class="stack">
      <h2>Finished, not merely working</h2>
      <p class="dim">Most software is shipped at the point it stops erroring. We are interested
        in the part after that &mdash; the copy that says what it means, the state nobody
        planned for, the second tap that should have been one.</p>
      <p class="dim">It is a small studio on purpose. You deal with the person doing the work,
        and the work is done in the open: you get the repository, the reasoning and a build
        every week.</p>
      <div class="actions">
        <a class="btn" href="studio.html">About the studio <span class="arw">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>
''')

# ------------------------------------------------------------------ work ----
write("work.html", "Work — Avodah",
      "Software released by Avodah, and how the studio works on client projects.",
      "work", f'''
<section class="hero flush">
  <div class="wrap">
    <p class="label label--accent">Work</p>
    <h1 style="margin-top:20px">Everything we have shipped.</h1>
    <p class="lede">The list is short because it is honest. An app appears here once it is
      on the App Store &mdash; not when it is announced, and not when it is nearly done.</p>
  </div>
</section>

<section class="flush" style="padding-top:0">
  <div class="wrap">
    <div class="ledger">
      <a class="entry rv" href="kilojo.html">
        <span class="n">01</span>
        <h3>Kilojo</h3>
        <p class="small dim">A food diary that reads your plate. Photograph a meal for an
          estimate, scan a barcode for the packet&rsquo;s own label, or type it in.</p>
        <span class="state">Coming soon</span>
      </a>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">Client work</p>
    <div class="stack">
      <h2>How a project runs</h2>
      <p class="dim">Client work is not listed publicly unless the client wants it to be.
        What is worth saying is how it goes.</p>
      <div class="grid grid-2" style="margin-top:8px">
        <div class="cell rv">
          <p class="label label--accent">Week one</p>
          <h4>Scope, written down</h4>
          <p class="small dim">Screens, states and what is explicitly out. A fixed price
            against that document, so the number does not move unless the scope does.</p>
        </div>
        <div class="cell rv">
          <p class="label label--accent">Every week</p>
          <h4>A build you can hold</h4>
          <p class="small dim">Installed on your own device, not a screenshot in a deck.
            You see it going wrong early enough to say so.</p>
        </div>
        <div class="cell rv">
          <p class="label label--accent">Release</p>
          <h4>Submission included</h4>
          <p class="small dim">App Store listing, privacy labels, review responses. The job
            is not done when the code is done.</p>
        </div>
        <div class="cell rv">
          <p class="label label--accent">After</p>
          <h4>You own all of it</h4>
          <p class="small dim">Repository, accounts, signing, the lot &mdash; documented well
            enough that another developer could pick it up without ringing us.</p>
        </div>
      </div>
      <div class="actions">
        <a class="btn btn--fill" href="contact.html">Start a project <span class="arw">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>
''')

# ---------------------------------------------------------------- kilojo ----
write("kilojo.html", "Kilojo — Avodah",
      "Kilojo is a food diary for iOS: photograph a meal for an estimate, or scan a barcode for the label.",
      "work", f'''
<section class="hero flush">
  <div class="wrap">
    <p class="label label--accent">01 &mdash; Kilojo &middot; iOS</p>
    <h1 style="margin-top:20px">A food diary that reads your plate.</h1>
    <p class="lede">Photograph a meal and Kilojo estimates the calories and macronutrients.
      Scan a barcode and it takes the figures straight off the packet. Everything it
      produces is editable, because an estimate you cannot correct is a guess you are
      stuck with.</p>
    <div class="actions">
      <a class="btn" href="contact.html">Ask about Kilojo <span class="arw">&rarr;</span></a>
    </div>
    <div class="meta">
      <div><span class="label">Platform</span><b>iOS</b></div>
      <div><span class="label">Price</span><b>Free</b></div>
      <div><span class="label">Status</span><b>Coming soon</b></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">Three ways in</p>
    <div class="grid grid-3">
      <div class="cell rv">
        <p class="label label--accent">Photograph</p>
        <h3>Point at the plate</h3>
        <p class="small dim">For food that never had a label &mdash; a plate of rice, a
          takeaway, someone else&rsquo;s cooking. Kilojo itemises what it can see and shows
          its working, so you can see why a number came out as it did.</p>
      </div>
      <div class="cell rv">
        <p class="label label--accent">Scan</p>
        <h3>Read the packet</h3>
        <p class="small dim">A barcode gives the manufacturer&rsquo;s own figures, which beats
          any estimate from a photograph. Instant, and free to run.</p>
      </div>
      <div class="cell rv">
        <p class="label label--accent">Type</p>
        <h3>Or just say it</h3>
        <p class="small dim">Sometimes you know. Type the name and the numbers, and log a
          repeat of it in one tap for as long as you keep eating it.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">Honestly</p>
    <div class="stack">
      <h2>What a photograph cannot tell you</h2>
      <p class="dim">A picture does not contain the portion. A bowl of rice can hold twice
        what it appears to, and no amount of cleverness recovers information the camera
        never captured. Kilojo estimates, and sometimes it is wrong.</p>
      <p class="dim">So it is built to be corrected: every figure is editable, it says how
        confident it is, and it shows the portion it assumed for each item rather than
        handing down a total. Tell it &ldquo;one cup of rice&rdquo; and the guess becomes
        arithmetic.</p>
      <div class="callout">
        <p class="small">Kilojo counts. It is not medical advice, and it does not have an
          opinion about your dinner.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">Privacy</p>
    <div class="stack">
      <h2>Your diary is yours</h2>
      <ul class="prose" style="padding-left:20px;display:grid;gap:8px;max-width:62ch">
        <li class="dim">No advertising, no analytics, no tracking software of any kind.</li>
        <li class="dim">Meal photographs are sent for analysis carrying the picture and your
          typed hint &mdash; not your name, your email or anything else about you.</li>
        <li class="dim">Barcode lookups send the number on the packet and nothing more.</li>
        <li class="dim">Erase everything, or delete the account outright, from inside the app.
          Both reach the server, not just the phone.</li>
      </ul>
      <div class="actions">
        <a class="btn" href="legal.html#privacy">Read the privacy policy <span class="arw">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>
''')

# ---------------------------------------------------------------- studio ----
write("studio.html", "Studio — Avodah",
      "Avodah is Hebrew for work, service and worship. One word for all three.",
      "studio", f'''
<section class="hero flush">
  <div class="wrap">
    <p class="label label--accent">Studio</p>
    <h1 style="margin-top:20px">Work, service, worship &mdash; one word.</h1>
    <p class="lede">Avodah is the Hebrew word for work. It is also the word for service, and
      for worship. Ancient Hebrew did not split them into separate ideas: the same word
      covered the craftsman at his bench and the offering he made.</p>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">The name</p>
    <div class="stack">
      <p class="dim">That distinction never made much sense here either. Work done carefully
        is worth something on its own terms, whoever is watching and whether or not anyone
        notices the part that took the longest.</p>
      <p class="dim">It is why nothing ships half-finished, why the code is written to be read
        by whoever comes next, and why one honest estimate beats winning a job on an
        optimistic one.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">How we work</p>
    <div class="grid grid-2">
      <div class="cell rv">
        <h4>You talk to the person building it</h4>
        <p class="small dim">No account manager relaying your question to someone who has not
          read the code. The studio is small on purpose and stays that way.</p>
      </div>
      <div class="cell rv">
        <h4>Scope in writing, price fixed to it</h4>
        <p class="small dim">Screens, states and what is deliberately excluded. The number
          moves only when the document does, and then you decide.</p>
      </div>
      <div class="cell rv">
        <h4>Working software every week</h4>
        <p class="small dim">On your device, not in a slide. The point is that you can tell
          us it is wrong while it is still cheap to change.</p>
      </div>
      <div class="cell rv">
        <h4>Everything handed over</h4>
        <p class="small dim">Repository, accounts, signing keys, and notes explaining the
          decisions &mdash; so you are never held hostage by the only person who understands it.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">Fit</p>
    <div class="stack">
      <h2>Who this suits</h2>
      <p class="dim">Founders and small teams with a clear idea and a real user in mind, who
        would rather have one considered thing than five rushed ones.</p>
      <p class="dim">Less good for projects that need twenty people by Friday, or for anyone
        wanting a body to fill a seat on an existing team.</p>
      <div class="actions">
        <a class="btn btn--fill" href="contact.html">Get in touch <span class="arw">&rarr;</span></a>
      </div>
    </div>
  </div>
</section>
''')

# --------------------------------------------------------------- contact ----
write("contact.html", "Contact — Avodah",
      "Support, new projects and acquisition enquiries for Avodah software studio.",
      "contact", f'''
<section class="hero flush">
  <div class="wrap">
    <p class="label label--accent">Contact</p>
    <h1 style="margin-top:20px">What brings you here?</h1>
    <p class="lede">Everything reaches the same inbox. Picking the closest fit just means a
      faster and more useful answer.</p>
  </div>
</section>

<section class="flush" style="padding-top:0">
  <div class="wrap">
    <div class="grid grid-3">
      <a class="cell rv" href="mailto:{MAIL}?subject=Support">
        <p class="label label--accent">Support</p>
        <h3>I use one of your apps</h3>
        <p class="small dim">Something is broken, a question about your account, or a feature
          you wish existed. Say which app and which phone.</p>
        <span class="go">{MAIL} <span class="arw">&rarr;</span></span>
      </a>
      <a class="cell rv" href="mailto:{MAIL}?subject=New%20project">
        <p class="label label--accent">New project</p>
        <h3>I want an app built</h3>
        <p class="small dim">The idea, who it is for, and roughly when it needs to be live.
          A budget range saves us both a round trip.</p>
        <span class="go">{MAIL} <span class="arw">&rarr;</span></span>
      </a>
      <a class="cell rv" href="mailto:{MAIL}?subject=Acquisition">
        <p class="label label--accent">Acquisition</p>
        <h3>I am interested in buying</h3>
        <p class="small dim">Enquiries about acquiring one of our apps, in whole or in part.</p>
        <span class="go">{MAIL} <span class="arw">&rarr;</span></span>
      </a>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <p class="label">Response</p>
    <div class="stack">
      <h2>What happens next</h2>
      <p class="dim">Support gets answered first, usually the same day. Project enquiries get
        a real reply rather than a calendar link &mdash; if it is not a fit we will say so
        and, where we can, point you somewhere better.</p>
      <p class="dim">Working directly with the person who writes the software: <a class="ln"
        href="mailto:{MAIL}">{MAIL}</a></p>
    </div>
  </div>
</section>
''')

# ----------------------------------------------------------------- legal ----
write("legal.html", "Privacy & Terms — Avodah",
      "Privacy policy and terms of use for Kilojo, by Avodah software studio.",
      "legal", f'''
<section class="hero flush">
  <div class="wrap">
    <p class="label label--accent">Kilojo</p>
    <h1 style="margin-top:20px">Privacy &amp; Terms</h1>
    <p class="lede">Kilojo is a food diary, so it holds things that are genuinely personal
      &mdash; what you eat, what you weigh, and photographs taken in your kitchen. This page
      says exactly what is held, where it goes and how to get rid of it.</p>
  </div>
</section>

<section class="flush" style="padding-top:0">
  <div class="wrap">
    <div class="todo">
      <p class="label label--accent">Before publishing — delete this box</p>
      <p class="small">Four values only you can fill in, marked through the page:
        <mark>[YOUR NAME OR COMPANY]</mark>, <mark>[SUPPORT EMAIL]</mark>,
        <mark>[YOUR COUNTRY]</mark>, <mark>[DATE]</mark>. Check the Anthropic section against
        their current terms. A careful draft written from what the app does &mdash; not legal
        advice.</p>
    </div>
  </div>
</section>

<section id="privacy">
  <div class="wrap split">
    <p class="label">Privacy policy</p>
    <div class="stack prose">
      <p class="small dim">Last updated <mark>[DATE]</mark> &middot; Kilojo for iOS &middot;
        Operated by <mark>[YOUR NAME OR COMPANY]</mark></p>

      <div class="callout">
        <p class="small"><b>Three things Kilojo does not do.</b> There is no advertising.
          There is no analytics or tracking software of any kind. Nothing about you is sold,
          rented or shared for marketing, by anyone, ever.</p>
      </div>

      <h3>What Kilojo holds</h3>
      <p class="dim small">Everything below is entered by you, or produced from something you
        entered. Kilojo does not read your contacts, your location or your health app.</p>
      <div class="scroll-x">
        <table>
          <tr><th>Email address</th><td class="dim">To sign in and reset a password</td></tr>
          <tr><th>Password</th><td class="dim">Stored hashed; never readable, including by us</td></tr>
          <tr><th>Meals</th><td class="dim">Name, description, calories, protein, carbs, fat, water, time</td></tr>
          <tr><th>Meal photographs</th><td class="dim">The picture you took, if you took one</td></tr>
          <tr><th>Weigh-ins</th><td class="dim">One weight per day, with its date</td></tr>
          <tr><th>Body details</th><td class="dim">Sex, age, height, weight, activity, goal &mdash; only if you build a plan</td></tr>
          <tr><th>Settings</th><td class="dim">Targets, reminder times, units, theme, your own note</td></tr>
        </table>
      </div>

      <h3>Where it is kept</h3>
      <p class="dim">On your phone first &mdash; Kilojo works without a connection, and your
        sign-in token lives in the iOS keychain. If you are signed in, a copy syncs to a
        Supabase project hosted on Amazon Web Services in <b>Tokyo, Japan</b>, so your diary
        survives a lost phone. If you are outside Japan, your data is transferred there.</p>
      <p class="dim">Each account can only reach its own rows and its own photographs, and
        that restriction is enforced by the database rather than by the app &mdash; so a fault
        in the app cannot expose one person&rsquo;s diary to another.</p>

      <h3>Who else sees it</h3>
      <p class="dim"><b>Anthropic</b>, for reading your photographs. The request carries the
        photograph and the hint you typed, and nothing else &mdash; not your name, your email,
        your account or your other meals. Scanning a barcode or typing a meal in sends nothing
        to Anthropic at all.</p>
      <p class="dim"><b>Supabase and Amazon Web Services</b>, for storage, on Kilojo&rsquo;s
        behalf and not for their own purposes.</p>
      <p class="dim"><b>Open Food Facts</b>, for barcodes. They receive the number printed on
        the packet and no account information, so they cannot tell who scanned it.</p>
      <p class="dim">Beyond these, data is disclosed only where the law requires it.</p>

      <h3>Deleting it</h3>
      <p class="dim"><b>Erase all data</b> clears your diary and keeps your login. <b>Delete my
        account</b> removes the account itself: photographs are deleted from storage first,
        then the account record and everything attached to it. Neither can be undone, and both
        reach the server rather than only the phone.</p>
      <div class="callout">
        <p class="small">When you delete a single meal, a marker is kept &mdash; its identifier
          and the fact of deletion, with no food, numbers or photograph attached. It exists so
          a second device learns the meal is gone rather than restoring it. These markers go
          when you delete your account.</p>
      </div>

      <h3>Your rights</h3>
      <ul>
        <li class="dim"><b>See it</b> &mdash; everything held is visible in the app.</li>
        <li class="dim"><b>Correct it</b> &mdash; every estimate is editable, by design.</li>
        <li class="dim"><b>Delete it</b> &mdash; both routes are in the app and need nobody&rsquo;s permission.</li>
        <li class="dim"><b>Take it elsewhere</b> &mdash; ask and you will be sent a machine-readable copy.</li>
      </ul>
      <p class="dim">In the UK and EU, the UK GDPR and GDPR give you these rights and the right
        to complain to your regulator. The basis for processing is the contract between us:
        without this data the app cannot do the thing you installed it for. Contact
        <mark>[SUPPORT EMAIL]</mark>.</p>

      <h3>Children</h3>
      <p class="dim">Kilojo is not intended for children under 13. Calorie tracking is not
        appropriate for everyone &mdash; if you have or have had an eating disorder, please
        speak to a doctor before using an app like this one.</p>
    </div>
  </div>
</section>

<section id="terms">
  <div class="wrap split">
    <p class="label">Terms of use</p>
    <div class="stack prose">
      <p class="small dim">Last updated <mark>[DATE]</mark></p>
      <p class="dim">By creating an account you agree to what follows. If you do not, please
        do not use the app.</p>

      <h3>About the numbers</h3>
      <div class="callout">
        <p class="small"><b>Kilojo estimates. It does not measure, and it is not medical
          advice.</b></p>
      </div>
      <p class="dim">A photograph cannot tell anyone how much food is on a plate; the app
        infers it and is sometimes wrong. Barcode figures come from a public database anyone
        may edit. Treat every number as a starting point to correct, which is why all of them
        are editable. Do not use Kilojo to make medical decisions or to replace advice from a
        doctor or dietitian.</p>

      <h3>Your account</h3>
      <ul>
        <li class="dim">Give a real email address &mdash; it is the only way to recover a password.</li>
        <li class="dim">Keep your password to yourself; activity through your account is treated as yours.</li>
        <li class="dim">You keep ownership of everything you put in.</li>
      </ul>

      <h3>Acceptable use</h3>
      <p class="dim">Do not attempt to reach another person&rsquo;s data, work around limits,
        take the service apart or automate it. Photo analysis is limited per person and per
        day; abusing it may end an account without warning.</p>

      <h3>Availability</h3>
      <p class="dim">Kilojo is provided as it is, with no warranty. It may be unavailable, may
        lose data, and may change or stop. To the fullest extent the law allows,
        <mark>[YOUR NAME OR COMPANY]</mark> is not liable for any loss arising from its use,
        including decisions taken on the strength of its estimates. Nothing here excludes
        liability that cannot lawfully be excluded.</p>

      <h3>Governing law</h3>
      <p class="dim">These terms are governed by the law of <mark>[YOUR COUNTRY]</mark>, and
        its courts have jurisdiction. Questions about either document:
        <mark>[SUPPORT EMAIL]</mark>.</p>
    </div>
  </div>
</section>
''')
