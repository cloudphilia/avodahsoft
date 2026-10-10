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
    Promise.race([fonts, new Promise((r) => setTimeout(r, 700))]).then(() => targets.forEach((el) => io.observe(el)));
  } else {
    targets.forEach((el) => { el.classList.add('in'); el.classList.remove('reveal'); });
  }

  // Phones on a stage drift at slightly different speeds as the page scrolls.
  const layers = [...document.querySelectorAll('[data-depth]')];
  if (layers.length && !still) {
    let ticking = false;
    const wide = window.matchMedia('(min-width: 700px)');
    const update = () => {
      ticking = false;
      const vh = window.innerHeight;
      for (const el of layers) {
        if (!wide.matches) { el.style.transform = ''; continue; }
        const r = el.parentElement.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) continue;
        const progress = (r.top + r.height / 2 - vh / 2) / vh;
        el.style.transform = `translate3d(0, ${(progress * parseFloat(el.dataset.depth)).toFixed(2)}px, 0)`;
      }
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
