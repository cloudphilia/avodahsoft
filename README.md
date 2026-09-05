# avodahsoft.com

Static site served by a Cloudflare Worker (Workers Assets) with a small contact API.

- `build.py` generates the pages into `public/` (run `python3 build.py`).
- `src/worker.js` handles redirects from legacy URLs, security headers, `www` → apex and `POST /api/contact` (Resend).
- `wrangler.jsonc` — worker `avodah-site`, custom domain `avodahsoft.com`. Secret: `RESEND_API_KEY` (`npx wrangler secret put RESEND_API_KEY`).
- Deploy: `python3 build.py && npx wrangler deploy`.

Photos are CC0 (StockSnap). App screenshots are our own.
