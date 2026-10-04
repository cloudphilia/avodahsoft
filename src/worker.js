/**
 * avodahsoft.com - static site on Workers Assets plus a tiny contact API (Resend).
 * Legacy URLs from the previous builds keep working via redirects.
 */
const REDIRECTS = {
  '/index.html': '/', '/work.html': '/work', '/studio.html': '/studio', '/contact.html': '/contact', '/kilojo.html': '/kilojo',
  '/legal.html': '/kilojo/privacy', '/legal/privacy': '/kilojo/privacy', '/legal/terms': '/kilojo/terms', '/legal/support': '/contact',
  '/legal': '/kilojo/privacy', '/work/kilojo': '/kilojo', '/work/gigpal': '/gigpal', '/privacy': '/gigpal/privacy', '/terms': '/gigpal/terms',
  // Papersuite was Kepta until 2026-10-04.
  '/kepta': '/papersuite', '/kepta/privacy': '/papersuite/privacy', '/kepta/terms': '/papersuite/terms',
};

const SECURITY_HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Frame-Options': 'DENY',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
};

/**
 * Universal Links for Kilojo and GigPal (each app has its own path, so they can't collide).
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
      {
        appIDs: ['7MG7R3644S.com.gigpal.app'],
        components: [
          { '/': '/gigpal/auth/callback', comment: 'GigPal email confirmation, change of address and password reset' },
          { '/': '/gigpal/auth/callback/', comment: 'the same, with a trailing slash' },
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
${KILOJO_PAGE_STYLE}
</head>
<body>
  <main class="card">
    <div class="mark" aria-hidden="true"></div>
    <h1 id="title">Checking your link…</h1>
    <p id="body"></p>
    <noscript><p>This page needs JavaScript to read your link. Open Kilojo on your phone and log in with your email and password.</p></noscript>
    <a class="btn" id="open" href="kilojo://auth/callback" hidden>Open Kilojo</a>
    <p class="foot">Kilojo — photograph a meal, get the calories back.</p>
  </main>
<script>
(function () {
  var q = new URLSearchParams(location.search);
  var h = new URLSearchParams(location.hash.replace(/^#/, ''));
  var failed = q.get('error_description') || h.get('error_description') || q.get('error') || h.get('error');
  var code = q.get('error_code') || h.get('error_code');
  var title = document.getElementById('title');
  var body = document.getElementById('body');
  var open = document.getElementById('open');

  // Set by the confirm page when its button was tapped, in this same tab. It is what
  // separates "you just confirmed your email" from a password-reset link, which lands on
  // this same page and has confirmed nothing.
  var confirming = false;
  try {
    confirming = sessionStorage.getItem('kilojo-confirming') === '1';
    sessionStorage.removeItem('kilojo-confirming');
  } catch (e) {}

  // Only the query goes to the app — a PKCE ?code=, useless on any phone but the one
  // that asked, or the reason a link was refused. Never the fragment: a session in the
  // fragment is exactly what a crafted link would use to sign someone into another account.
  open.href = 'kilojo://auth/callback' + location.search;
  // Only where there could be a Kilojo to open. On a laptop the button is a dead end, and
  // a dead end is exactly what this page exists to replace. iPadOS reports itself as a
  // Mac, so a touch screen counts too.
  open.hidden = !(/iPhone|iPad|iPod|Android/i.test(navigator.userAgent) || navigator.maxTouchPoints > 1);

  if (failed && code === 'otp_expired' && confirming) {
    title.textContent = 'This link has expired';
    body.innerHTML = 'Confirmation links last an hour. Open Kilojo on your phone and tap ' +
      '\\u201cResend the confirmation email\\u201d for a fresh one, or log in \\u2014 if you confirmed ' +
      'already, that is all it takes.';
  } else if (failed) {
    title.textContent = 'This link no longer works';
    body.innerHTML = 'Links in email work once and expire after an hour. Open Kilojo on your phone and log in. ' +
      'If it says you are not confirmed yet, ask for a fresh email there.';
  } else if (confirming) {
    title.textContent = 'Your email is confirmed';
    body.innerHTML = 'That is the account done. Go back to Kilojo on your phone \\u2014 it carries on ' +
      'by itself. If it does not, log in with the email and password you chose.';
  } else {
    title.textContent = 'Open Kilojo to carry on';
    body.innerHTML = 'Finish this on the phone that asked for the email: open Kilojo there. ' +
      'A password reset only works on that phone.';
  }
})();
</script>
</body>
</html>`;
}

/**
 * The page an emailed confirmation link lands on first, before anything is spent.
 *
 * It used to be a 302 straight to Supabase's verify endpoint, and mail providers follow
 * every URL in an inbox within seconds of delivery — so the single-use token was gone
 * before the person ever tapped it. Scanners fetch; they do not press buttons. The verify
 * call now waits for a tap.
 *
 * Where it sends people afterwards is fixed here, not taken from the link: builds already
 * in the App Store ask for `kilojo://auth/callback`, which is a dead end on any device
 * without Kilojo — a laptop, or the other phone the inbox lives on. Confirmation is
 * recorded server-side either way, so the callback page can honestly say it is done.
 *
 * As with the callback page, the button is built in the browser from `location`, so no
 * part of the link is interpolated into this HTML on the server.
 */
function authConfirmPage() {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Kilojo</title>
${KILOJO_PAGE_STYLE}
</head>
<body>
  <main class="card">
    <div class="mark" aria-hidden="true"></div>
    <h1>Confirm your email</h1>
    <p>One tap and your Kilojo account is ready. You can do this on any device.</p>
    <noscript><p>This page needs JavaScript to confirm your address. Turn it on, or open the email on your phone.</p></noscript>
    <a class="btn" id="confirm" href="#">Confirm my email</a>
    <p class="foot">Kilojo — photograph a meal, get the calories back.</p>
  </main>
<script>
(function () {
  var q = new URLSearchParams(location.search);
  var verify = new URLSearchParams({
    token: q.get('token') || '',
    type: q.get('type') || '',
    redirect_to: '${AUTH_CALLBACK_URL}',
  });
  var button = document.getElementById('confirm');
  button.href = '${SUPABASE_VERIFY_URL}?' + verify.toString();
  // Tells the callback page, in this tab, that it is showing the end of a confirmation.
  button.addEventListener('click', function () {
    try { sessionStorage.setItem('kilojo-confirming', '1'); } catch (e) {}
  });
})();
</script>
</body>
</html>`;
}

const AUTH_CALLBACK_URL = 'https://avodahsoft.com/auth/callback';
const SUPABASE_VERIFY_URL = 'https://axruyecaabpyddxwzfbz.supabase.co/auth/v1/verify';
/** Link types that only confirm an address, and so can finish on any device. */
const CONFIRM_TYPES = new Set(['signup', 'email_change']);

const KILOJO_PAGE_STYLE = `<style>
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
</style>`;

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

/**
 * GigPal's auth emails link straight to its Universal Link, https://avodahsoft.com/gigpal/auth/callback.
 * On an iPhone with GigPal the app takes it (and verifies the token itself). Anywhere else this one
 * route plays both parts: from the email (token_hash + type) it waits for a tap before verifying
 * anything, since mail scanners fetch links but don't press buttons; after Supabase verifies, it is
 * where Supabase sends people back, and says what happened. Everything is built in the browser from
 * `location`; nothing from the link is interpolated on the server.
 */
const GIGPAL_VERIFY_URL = 'https://therszyqjgwyaxhcjvmt.supabase.co/auth/v1/verify';
const GIGPAL_CALLBACK_URL = 'https://avodahsoft.com/gigpal/auth/callback';

function gigpalAuthPage() {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>GigPal</title>
<style>
  :root { color-scheme: dark; --bg:#0E1230; --surface:#141A3D; --line:rgba(255,255,255,0.08); --text:#F5F6FF; --muted:#AEB4DA; --accent:#FF8A3D; }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:grid; place-items:center; padding:24px; background:var(--bg); color:var(--text);
         font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  .card { width:100%; max-width:26rem; background:var(--surface); border:1px solid var(--line); border-radius:20px; padding:32px 26px; text-align:center; }
  .mark { width:56px; height:56px; border-radius:16px; margin:0 auto 18px; background:linear-gradient(145deg,#FFB061,#FF5E62); }
  h1 { font-size:1.35rem; margin:0 0 10px; }
  p { margin:0 0 14px; color:var(--muted); }
  .btn { display:block; margin:22px 0 0; padding:14px 18px; border-radius:999px; background:var(--accent); color:#0E1230; font-weight:700; text-decoration:none; }
  .foot { margin:18px 0 0; font-size:0.8rem; color:var(--muted); }
</style>
</head>
<body>
  <main class="card">
    <div class="mark" aria-hidden="true"></div>
    <h1 id="title">Checking your link…</h1>
    <p id="body"></p>
    <noscript><p>This page needs JavaScript to read your link. Open GigPal on your phone and sign in with your email and password.</p></noscript>
    <a class="btn" id="go" href="#" hidden></a>
    <p class="foot">GigPal — the practice room in your pocket.</p>
  </main>
<script>
(function () {
  var q = new URLSearchParams(location.search);
  var h = new URLSearchParams(location.hash.replace(/^#/, ''));
  var title = document.getElementById('title'), body = document.getElementById('body'), go = document.getElementById('go');
  var phone = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) || navigator.maxTouchPoints > 1;
  function show(t, b, label, href, onTap) {
    title.textContent = t; body.textContent = b;
    if (label) { go.textContent = label; go.href = href; go.hidden = false; if (onTap) go.addEventListener('click', onTap); }
  }
  function verify(redirect) {
    return '${GIGPAL_VERIFY_URL}?' + new URLSearchParams({ token: q.get('token_hash') || '', type: q.get('type') || '', redirect_to: redirect }).toString();
  }

  // 1. Straight from the email: wait for a tap.
  if (q.get('token_hash')) {
    var type = q.get('type');
    if (type === 'signup' || type === 'email_change') {
      show(type === 'signup' ? 'Confirm your email' : 'Confirm your new email',
        'One tap and your GigPal account is ready. This works on any device — GigPal on your phone signs you in by itself a moment later.',
        type === 'signup' ? 'Confirm my email' : 'Confirm new email', verify('${GIGPAL_CALLBACK_URL}'),
        function () { try { sessionStorage.setItem('gigpal-confirming', '1'); } catch (e) {} });
    } else if (type === 'recovery' && phone) {
      // Builds from before this change exchange the PKCE code on the phone that asked.
      show('Choose a new password', 'Open GigPal to set a new password. This only works on the phone that asked for the reset.',
        'Open GigPal', verify('gigpal://auth-callback'));
    } else {
      show('Open this on your phone', 'Password resets finish in GigPal. Open this email on the iPhone with GigPal installed and tap the button there.');
    }
    return;
  }

  // 2. Supabase sending people back after verifying.
  var failed = q.get('error_description') || h.get('error_description') || q.get('error') || h.get('error');
  var code = q.get('error_code') || h.get('error_code');
  var confirming = false;
  try { confirming = sessionStorage.getItem('gigpal-confirming') === '1'; sessionStorage.removeItem('gigpal-confirming'); } catch (e) {}
  // Only the query goes to the app (a PKCE ?code=, useless on any phone but the one that asked),
  // never the fragment: a session in the fragment is what a crafted link would use.
  var open = phone && q.get('code') ? 'gigpal://auth-callback?' + new URLSearchParams({ code: q.get('code') }).toString() : null;

  if (failed && code === 'otp_expired' && confirming) {
    show('This link has expired', 'Confirmation links last an hour. Open GigPal on your phone and tap “Send it again” for a fresh one — or just sign in: if you confirmed already, that is all it takes.');
  } else if (failed) {
    show('This link no longer works', 'Links in email work once and expire after an hour. Open GigPal on your phone and sign in; if it says you are not confirmed yet, ask for a fresh email there.');
  } else if (confirming) {
    show('Your email is confirmed', 'That is the account done. Go back to GigPal on your phone — it carries on by itself. If it does not, sign in with the email and password you chose.',
      open && 'Open GigPal', open);
  } else {
    show('Open GigPal to carry on', 'Finish this on the phone that asked for the email: open GigPal there.', open && 'Open GigPal', open);
  }
})();
</script>
</body>
</html>`;
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
      if (CONFIRM_TYPES.has(type)) {
        return new Response(authConfirmPage(), {
          headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', ...SECURITY_HEADERS },
        });
      }
      // A password reset has to finish where the app is, so it still goes straight through.
      const q = new URLSearchParams({ token, type });
      if (redirectTo) q.set('redirect_to', redirectTo);
      return Response.redirect(`https://axruyecaabpyddxwzfbz.supabase.co/auth/v1/verify?${q}`, 302);
    }
    if (path === '/gigpal/auth/callback') {
      const p = url.searchParams;
      const tokenHash = p.get('token_hash');
      // A link from the email carries token_hash + type; anything else is Supabase sending people back.
      if (tokenHash !== null && (!/^[A-Za-z0-9_-]{8,}$/.test(tokenHash) || !/^[a-z_]{1,32}$/.test(p.get('type') || ''))) {
        return new Response('Bad link', { status: 400 });
      }
      return new Response(gigpalAuthPage(), {
        headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', ...SECURITY_HEADERS, 'Referrer-Policy': 'no-referrer' },
      });
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
