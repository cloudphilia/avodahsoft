/**
 * avodahsoft.com - static site on Workers Assets plus a tiny contact API (Resend).
 * Legacy URLs from the previous builds keep working via redirects.
 */
const REDIRECTS = {
  '/index.html': '/', '/work.html': '/work', '/studio.html': '/studio', '/contact.html': '/contact', '/kilojo.html': '/kilojo',
  '/legal.html': '/kilojo/privacy', '/legal/privacy': '/kilojo/privacy', '/legal/terms': '/kilojo/terms', '/legal/support': '/contact',
  '/legal': '/kilojo/privacy', '/work/kilojo': '/kilojo', '/work/gigpal': '/gigpal', '/privacy': '/gigpal/privacy', '/terms': '/gigpal/terms',
};

const SECURITY_HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Frame-Options': 'DENY',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
};

const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...SECURITY_HEADERS } });
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
// Strip control characters (except newline and tab) and clamp the length.
const CONTROL_RE = new RegExp('[\\u0000-\\u0008\\u000B\\u000C\\u000E-\\u001F\\u007F]', 'g');
const clean = (v, max) => String(v ?? '').replace(CONTROL_RE, '').trim().slice(0, max);

async function handleContact(request, env) {
  if (request.method !== 'POST') return json({ ok: false, error: 'Method not allowed' }, 405);
  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: 'Invalid request' }, 400);
  }
  if (clean(data.website, 10)) return json({ ok: true }); // honeypot: pretend success
  const name = clean(data.name, 120);
  const email = clean(data.email, 200);
  const topic = clean(data.topic, 60) || 'General';
  const message = clean(data.message, 5000);
  if (name.length < 2) return json({ ok: false, error: 'Please tell us your name.' }, 400);
  if (!EMAIL_RE.test(email)) return json({ ok: false, error: 'That email address does not look right.' }, 400);
  if (message.length < 10) return json({ ok: false, error: 'Please add a little more detail.' }, 400);
  if (!env.RESEND_API_KEY) return json({ ok: false, error: 'Mail is not configured yet. Email hello@avodahsoft.com.' }, 503);
  const to = env.CONTACT_TO || 'hello@avodahsoft.com';
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const country = request.headers.get('CF-IPCountry') || '';
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'Avodahsoft website <no-reply@avodahsoft.com>',
      to: [to],
      reply_to: email,
      subject: `[avodahsoft.com] ${topic} - ${name}`,
      text: `${message}\n\n--\nFrom: ${name} <${email}>\nTopic: ${topic}\nIP: ${ip} ${country}\nPage: ${request.headers.get('Referer') || ''}`,
    }),
  });
  if (!res.ok) return json({ ok: false, error: 'Could not send right now. Email hello@avodahsoft.com instead.' }, 502);
  return json({ ok: true });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname.startsWith('www.')) return Response.redirect(`https://${url.hostname.slice(4)}${url.pathname}${url.search}`, 301);
    const path = url.pathname.replace(/\/+$/, '') || '/';
    if (REDIRECTS[path]) return Response.redirect(`${url.origin}${REDIRECTS[path]}`, 301);
    if (path === '/api/contact') return handleContact(request, env);
    const res = await env.ASSETS.fetch(request);
    const headers = new Headers(res.headers);
    for (const [k, v] of Object.entries(SECURITY_HEADERS)) headers.set(k, v);
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
  },
};
