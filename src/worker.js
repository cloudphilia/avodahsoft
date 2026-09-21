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

/**
 * Universal Links for Kilojo.
 *
 * Served from the worker rather than as a static asset so the content type is certainly
 * `application/json` and the path is certainly un-redirected — iOS fetches this file once,
 * refuses anything else, and then silently never opens the app again.
 *
 * With this in place an auth link on an iPhone that has Kilojo opens Kilojo itself, with
 * no "this site is trying to open another application" prompt in between. On a laptop, or
 * a phone without the app, the same URL is an ordinary web page: see `authCallbackPage`.
 */
const APPLE_APP_SITE_ASSOCIATION = {
  applinks: {
    details: [
      {
        appIDs: ['7MG7R3644S.com.kilojo.app'],
        components: [
          { '/': '/auth/callback', comment: 'Kilojo email confirmation and password reset' },
          { '/': '/auth/callback/*', comment: 'the same, with a trailing path' },
        ],
      },
    ],
  },
};

/**
 * Where Supabase sends people after it has verified an emailed link.
 *
 * Reached only when the app did not take the link first, which means one of two things:
 * the device has no Kilojo on it, or it has a build from before Universal Links. Either
 * way the verification has already happened server-side by the time this renders — the
 * address is confirmed, whatever the browser does next — so the page's job is to say so
 * and point at the phone.
 *
 * The hand-off button is built in the browser from `location`, so no part of the link is
 * interpolated into this HTML on the server.
 */
function authCallbackPage() {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Kilojo</title>
<style>
  :root { color-scheme: dark; --bg:#0A0C11; --surface:#141821; --line:#222838; --text:#F2F4F8; --muted:#9AA3B5; --ember:#FF6A3D; }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:grid; place-items:center; padding:24px;
         background:var(--bg); color:var(--text);
         font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  .card { width:100%; max-width:26rem; background:var(--surface); border:1px solid var(--line);
          border-radius:20px; padding:32px 26px; text-align:center; }
  .mark { width:56px; height:56px; border-radius:16px; margin:0 auto 18px;
          background:linear-gradient(145deg,#FF9A4D,#E8501F); }
  h1 { font-size:1.35rem; margin:0 0 10px; letter-spacing:-0.01em; }
  p { margin:0 0 14px; color:var(--muted); }
  .btn { display:block; margin:22px 0 0; padding:14px 18px; border-radius:999px;
         background:var(--ember); color:#11131A; font-weight:700; text-decoration:none; }
  .foot { margin:18px 0 0; font-size:0.8rem; color:var(--muted); }
  a.plain { color:var(--ember); }
</style>
</head>
<body>
  <main class="card">
    <div class="mark" aria-hidden="true"></div>
    <h1 id="title">Checking your link…</h1>
    <p id="body"></p>
    <a class="btn" id="open" href="kilojo://auth/callback">Open Kilojo</a>
    <p class="foot">Kilojo — photograph a meal, get the calories back.</p>
  </main>
<script>
(function () {
  var q = new URLSearchParams(location.search);
  var h = new URLSearchParams(location.hash.replace(/^#/, ''));
  var failed = q.get('error_description') || h.get('error_description') || q.get('error') || h.get('error');
  var title = document.getElementById('title');
  var body = document.getElementById('body');
  var open = document.getElementById('open');

  // Whatever the link carried, hand the whole thing to the app unchanged. A build from
  // before Universal Links still reads its confirmation out of this custom-scheme URL.
  open.href = 'kilojo://auth/callback' + location.search + location.hash;

  if (failed) {
    title.textContent = 'This link has already been used';
    body.innerHTML = 'Links in email are single-use, and mail apps often follow them before you do \u2014 ' +
      'which usually means your address <strong>is</strong> already confirmed. ' +
      'Open Kilojo on your phone and log in. If it still says you are not confirmed, ask for a fresh link there.';
  } else {
    title.textContent = 'Your email is confirmed';
    body.innerHTML = 'That is the account done. Open Kilojo on your phone and log in with the ' +
      'email and password you chose.';
  }
})();
</script>
</body>
</html>`;
}

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

/**
 * Keep free-tier Supabase projects from being paused for inactivity: a cron trigger runs a
 * real (RLS-scoped, empty) query against each project every few hours.
 * KEEPALIVE_TARGETS is a secret holding a JSON array of { name, url, key, rpc } (publishable
 * keys). Each project carries a `public.keepalive()` function granted to anon — a no-op
 * returning now(), so the ping is a real Postgres round trip that answers 200. Leaning on a
 * function the app owns instead would tie the cron to a signature the app may change.
 */
async function keepAlive(env) {
  let targets = [];
  try { targets = JSON.parse(env.KEEPALIVE_TARGETS || '[]'); } catch { targets = []; }
  const results = [];
  for (const t of targets) {
    if (!t?.url || !t?.key) continue;
    const base = String(t.url).replace(/\/+$/, '');
    try {
      // Legacy anon keys are JWTs and go in Authorization too; new publishable keys (sb_publishable_…) only use apikey.
      const headers = { apikey: t.key, ...(String(t.key).startsWith('eyJ') ? { Authorization: `Bearer ${t.key}` } : {}), Accept: 'application/json', 'User-Agent': 'avodahsoft-keepalive/1.0' };
      // Prefer an anon-callable RPC (a real Postgres round-trip that returns 200); fall back to a table select.
      const res = t.rpc
        ? await fetch(`${base}/rest/v1/rpc/${t.rpc}`, { method: 'POST', headers: { ...headers, 'Content-Type': 'application/json' }, body: JSON.stringify(t.body || {}), signal: AbortSignal.timeout(15000) })
        : await fetch(`${base}/rest/v1/${t.table || 'profiles'}?select=id&limit=1`, { headers, signal: AbortSignal.timeout(15000) });
      results.push({ name: t.name || base, status: res.status });
    } catch (err) {
      results.push({ name: t.name || base, error: String(err?.message || err) });
    }
  }
  console.log('keepalive', JSON.stringify(results));
  return results;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname.startsWith('www.')) return Response.redirect(`https://${url.hostname.slice(4)}${url.pathname}${url.search}`, 301);
    const path = url.pathname.replace(/\/+$/, '') || '/';
    // Auth links in Kilojo's emails point here, on our own domain, and are forwarded to
    // Supabase's verify endpoint. Only the three fields the template writes are passed on;
    // the token is single-use and expires, so the link is safe to carry in the open.
    if (path === '/.well-known/apple-app-site-association') {
      return new Response(JSON.stringify(APPLE_APP_SITE_ASSOCIATION), {
        headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=3600', ...SECURITY_HEADERS },
      });
    }
    if (path === '/auth/callback') {
      return new Response(authCallbackPage(), {
        headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', ...SECURITY_HEADERS },
      });
    }
    if (path === '/auth/kilojo') {
      const p = url.searchParams;
      const token = p.get('token') || '';
      const type = p.get('type') || '';
      const redirectTo = p.get('redirect_to') || '';
      if (!/^[A-Za-z0-9_-]{8,}$/.test(token) || !/^[a-z_]{1,32}$/.test(type)) return new Response('Bad link', { status: 400 });
      const q = new URLSearchParams({ token, type });
      if (redirectTo) q.set('redirect_to', redirectTo);
      return Response.redirect(`https://axruyecaabpyddxwzfbz.supabase.co/auth/v1/verify?${q}`, 302);
    }
    if (REDIRECTS[path]) return Response.redirect(`${url.origin}${REDIRECTS[path]}`, 301);
    if (path === '/api/contact') return handleContact(request, env);
    const res = await env.ASSETS.fetch(request);
    const headers = new Headers(res.headers);
    for (const [k, v] of Object.entries(SECURITY_HEADERS)) headers.set(k, v);
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
  },
  async scheduled(event, env, ctx) {
    ctx.waitUntil(keepAlive(env));
  },
};
