(() => {
  const root = document.documentElement;
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Navigation: the bar fades in once the page moves; the menu opens over the page on phones.
  const nav = document.querySelector('.nav');
  const burger = document.querySelector('.burger');
  const links = document.querySelector('.links');
  const onScroll = () => nav && nav.classList.toggle('scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  const setMenu = (open) => {
    links.classList.toggle('open', open);
    nav.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
  };
  // The black pill marks the page you are on. It slides to a new page the moment that page is
  // clicked, while it loads, rather than waiting for the next page to appear.
  const pill = links && links.querySelector('.nav-pill');
  const wideNav = window.matchMedia('(min-width: 881px)');
  const current = () => links && links.querySelector('a[aria-current]');
  const place = (a, animate) => {
    if (!pill) return;
    if (!a || !wideNav.matches) { pill.classList.remove('on'); return; }
    if (!animate) pill.classList.add('still');
    pill.style.width = a.offsetWidth + 'px';
    pill.style.height = a.offsetHeight + 'px';
    pill.style.transform = `translate(${a.offsetLeft}px, ${a.offsetTop}px)`;
    pill.classList.add('on');
    links.classList.add('pill-ready');
    if (!animate) requestAnimationFrame(() => requestAnimationFrame(() => pill.classList.remove('still')));
  };
  if (pill) {
    const here = current();
    place(here, false);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => place(current(), false));
    window.addEventListener('resize', () => place(current(), false));
    // The next page is fetched while the pointer rests on its menu item, so the change is near instant.
    const fetched = new Set();
    const prefetch = (a) => {
      if (!a || fetched.has(a.href) || a.origin !== location.origin) return;
      fetched.add(a.href);
      const l = document.createElement('link');
      l.rel = 'prefetch'; l.href = a.href;
      document.head.appendChild(l);
    };
    links.addEventListener('mouseover', (e) => prefetch(e.target.closest('a')));
    links.addEventListener('focusin', (e) => prefetch(e.target.closest('a')));
    // Click: the pill glides to the new item first, then the page changes underneath it. The new
    // page draws its pill in the same place, so the hand-over is seamless.
    links.addEventListener('click', (e) => {
      const a = e.target.closest('a');
      if (!a || !wideNav.matches || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const was = current();
      if (was === a) return;
      if (was) was.removeAttribute('aria-current');
      a.setAttribute('aria-current', 'page');
      place(a, Boolean(was));
      if (!still) { e.preventDefault(); setTimeout(() => { location.href = a.href; }, was ? 300 : 140); }
    });
    // Coming back with the Back button shows this page's own item again, not the one clicked.
    window.addEventListener('pageshow', (e) => {
      if (!e.persisted) return;
      links.querySelectorAll('a[aria-current]').forEach((x) => x.removeAttribute('aria-current'));
      if (here) here.setAttribute('aria-current', 'page');
      place(here, false);
    });
  }

  if (burger && links) {
    burger.addEventListener('click', () => setMenu(!links.classList.contains('open')));
    links.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && links.classList.contains('open')) setMenu(false); });
    window.matchMedia('(min-width: 881px)').addEventListener('change', (m) => { if (m.matches) setMenu(false); });
  }

  // Headlines marked .words rise word by word out of a mask.
  document.querySelectorAll('.words').forEach((el) => {
    let i = 0;
    const walk = (node) => {
      for (const child of [...node.childNodes]) {
        if (child.nodeType === 1) { walk(child); continue; }
        if (child.nodeType !== 3) continue;
        const frag = document.createDocumentFragment();
        for (const part of child.textContent.split(/(\s+)/)) {
          if (!part) continue;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); continue; }
          const w = document.createElement('span');
          const inner = document.createElement('span');
          w.className = 'w';
          inner.textContent = part;
          inner.style.setProperty('--wi', i++);
          w.appendChild(inner);
          frag.appendChild(w);
        }
        child.replaceWith(frag);
      }
    };
    walk(el);
    el.classList.add('is-split');
  });

  // Children of a [data-stagger] group arrive one after another.
  document.querySelectorAll('[data-stagger]').forEach((group) => {
    [...group.querySelectorAll(':scope > .reveal')].forEach((el, i) => el.style.setProperty('--i', i));
  });

  // The demo video sits inside a phone: a play button until it starts, then the usual controls.
  document.querySelectorAll('.film-device').forEach((frame) => {
    const video = frame.querySelector('video');
    const play = frame.querySelector('.play');
    if (!video || !play) return;
    video.controls = false;
    play.hidden = false;
    const start = () => { play.hidden = true; video.controls = true; video.play().catch(() => {}); };
    play.addEventListener('click', start);
    video.addEventListener('play', () => { play.hidden = true; video.controls = true; });
  });

  // Elements arrive as they scroll into view. Once an entrance has finished, its styling is
  // removed, so hover effects answer at once instead of inheriting the entrance's timing.
  const targets = document.querySelectorAll('.reveal, .words');
  const settle = (el) => {
    if (!el.classList.contains('reveal')) return;
    const wait = 1700 + (parseFloat(el.style.getPropertyValue('--i')) || 0) * 90;
    setTimeout(() => el.classList.remove('reveal'), wait);
  };
  const show = (el) => { el.classList.add('in'); settle(el); };
  if ('IntersectionObserver' in window && !still) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    // Start once the fonts are in (or after a moment), so letters never change shape mid-animation.
    const fonts = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
    Promise.race([fonts, new Promise((r) => setTimeout(r, 250))]).then(() => targets.forEach((el) => io.observe(el)));
  } else {
    targets.forEach((el) => { el.classList.add('in'); el.classList.remove('reveal'); });
  }

  // Phones on a stage drift at slightly different speeds as the page scrolls.
  const layers = [...document.querySelectorAll('[data-depth]')];
  if (layers.length && !still) {
    let ticking = false;
    const wide = window.matchMedia('(min-width: 700px)');
    const depths = layers.map((el) => parseFloat(el.dataset.depth) || 0);
    const update = () => {
      ticking = false;
      if (!wide.matches) { layers.forEach((el) => { el.style.transform = ''; }); return; }
      // Read every position first, then write, so the browser lays the page out once per frame.
      const vh = window.innerHeight;
      const rects = layers.map((el) => el.parentElement.getBoundingClientRect());
      rects.forEach((r, i) => {
        if (r.bottom < -200 || r.top > vh + 200) return;
        const progress = (r.top + r.height / 2 - vh / 2) / vh;
        layers[i].style.transform = `translate3d(0, ${(progress * depths[i]).toFixed(1)}px, 0)`;
      });
    };
    const request = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', request);
    update();
  }

  // Legal pages: the contents list follows the section being read.
  const toc = document.querySelector('.toc');
  if (toc && 'IntersectionObserver' in window) {
    const items = new Map([...toc.querySelectorAll('a')].map((a) => [a.getAttribute('href').slice(1), a]));
    const seen = new Set();
    const spy = new IntersectionObserver((entries) => {
      for (const e of entries) e.isIntersecting ? seen.add(e.target.id) : seen.delete(e.target.id);
      const first = [...items.keys()].find((id) => seen.has(id));
      if (first) items.forEach((a, id) => a.classList.toggle('on', id === first));
    }, { rootMargin: '-20% 0px -65% 0px' });
    items.forEach((_, id) => { const h = document.getElementById(id); if (h) spy.observe(h); });
  }

  const form = document.querySelector('form[data-contact]');
  if (form) {
    const status = form.querySelector('.status');
    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      const btn = form.querySelector('button[type=submit]');
      btn.disabled = true; status.textContent = 'Sending...'; status.className = 'status';
      try {
        const res = await fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        const body = await res.json().catch(() => ({}));
        if (!res.ok || !body.ok) throw new Error(body.error || 'Could not send');
        status.textContent = 'Thank you. Your message is in, and we reply to every one, usually the same day.'; status.className = 'status ok'; form.reset();
      } catch (err) {
        status.textContent = (err && err.message) || 'Something went wrong. Email hello@avodahsoft.com instead.'; status.className = 'status err';
      } finally { btn.disabled = false; }
    });
  }
  const y = document.querySelector('[data-year]'); if (y) y.textContent = String(new Date().getFullYear());
  root.classList.add('ready');
})();
