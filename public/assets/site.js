(() => {
  const burger = document.querySelector('.burger');
  const links = document.querySelector('.links');
  if (burger && links) burger.addEventListener('click', () => { const open = links.classList.toggle('open'); burger.setAttribute('aria-expanded', String(open)); });

  const io = 'IntersectionObserver' in window ? new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }, { threshold: 0.12 }) : null;
  document.querySelectorAll('.reveal').forEach((el) => (io ? io.observe(el) : el.classList.add('in')));

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
        status.textContent = 'Thanks - your message is in. We reply to every one, usually the same day.'; status.className = 'status ok'; form.reset();
      } catch (err) {
        status.textContent = (err && err.message) || 'Something went wrong. Email hello@avodahsoft.com instead.'; status.className = 'status err';
      } finally { btn.disabled = false; }
    });
  }
  const y = document.querySelector('[data-year]'); if (y) y.textContent = String(new Date().getFullYear());
})();
