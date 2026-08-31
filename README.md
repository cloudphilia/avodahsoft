# avodahsoft.com

The studio site. Static HTML, no build step at deploy time — GitHub Pages serves
these files as they are.

- `assets/site.css` — the whole design system. One grotesk, one mono, cool paper,
  a single deep green. Light and dark both defined at token level.
- `build.py` — emits the pages so the shell, nav and footer cannot drift apart.
  Edit the content in there, run `python3 build.py`, commit what it writes.
- `legal.html` — Kilojo's privacy policy and terms. Placeholders are marked and
  listed in a box at the top of the page; that box comes out before launch.

Deployed from `main`, root folder.
