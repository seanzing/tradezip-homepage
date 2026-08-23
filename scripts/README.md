# tradezip-homepage scripts

## `onboard-industry-page.py`

Ingest a new industry landing page from a ChatGPT-generated HTML file (or any raw single-file HTML) and slim it down to site standards.

### What it does

1. **Font extraction** — every `@font-face { src: url(data:font/woff2;base64,...) }` block gets its bytes written to `/assets/fonts/{family}-{weight}-{style}-{subset}.woff2` and the `src:` rewritten to a URL. Fonts are deduped by content hash across pages so we ship one shared font pool for the whole site.

2. **Work-showcase image extraction** — every `.rf-work-image` card's inline base64 image gets extracted to `/assets/{industry}/work/{alt-slug}.webp` (converted via `cwebp` if available, otherwise the original format) and the `<img src>` rewritten. Deduped by hash.

3. **Pricing tier CTAs** — every `Choose Local`/`Choose Growth`/`Choose Complete` anchor pointing at `#contact` or `#consultation` gets rewritten to point at the LIVE Stripe payment link on `checkout.zing.work`, with `target="_blank" rel="noopener" data-tier="…"` and the label changed to `Buy Now`.

### Usage

```bash
cd ~/Projects/tradezip-site
python3 scripts/onboard-industry-page.py <industry-slug> <path-to-source-html>

# example
python3 scripts/onboard-industry-page.py plumbers /tmp/plumbers-from-chatgpt.html

# dry-run to preview without writing files
python3 scripts/onboard-industry-page.py plumbers /tmp/plumbers-from-chatgpt.html --dry-run
```

Output lands at `web-design/{industry}/index.html`, with assets under `assets/fonts/` and `assets/{industry}/work/`.

### Typical size savings

A raw ChatGPT-generated industry page is ~22 MB (fonts + hero images inlined as base64). After this script:

- Fonts extracted: ~194 KB out of the HTML into shared `/assets/fonts/`
- Work images: ~5 MB of PNG → ~500 KB WebP (dedicated files, cacheable)
- Final HTML: ~8-9 MB — mostly the remaining inline hero + testimonial imagery not covered by the extraction patterns

### Idempotency

Safe to re-run against an already-processed file — hashes are checked, no duplicate assets are created, and the pricing-CTA regex only matches the pre-Stripe `Choose Local/Growth/Complete → #contact/#consultation` pattern (which is gone after the first pass).

### Dependencies

- `python3` (stdlib only, no pip)
- `cwebp` (optional, from Homebrew's `webp` package). Without it, images are extracted in their original PNG/JPG format — still cacheable, just larger.

### Adding a new page: end-to-end workflow

1. Amy generates HTML in ChatGPT for `plumbers`
2. She sends the file (or drops it in `~/Downloads/`)
3. I run: `python3 scripts/onboard-industry-page.py plumbers ~/Downloads/plumbers-chatgpt.html`
4. Local preview: `python3 -m http.server 8080` then visit `http://127.0.0.1:8080/web-design/plumbers/`
5. Screenshot check at 390 / 1440 via puppeteer
6. `git add` → commit → PR → merge → GH Pages deploy

### Related: Stripe payment links (source of truth)

Set at product-creation time on 2026-08-23 (see `memory/2026-08-23.md` in the workspace):

- Local ($79/mo):    `https://checkout.zing.work/b/4gMeVe7BSdOP6FK0sL5J60K`  →  `price_1U7UnRJdCDYxERim7BGveG0s`
- Growth ($129/mo):  `https://checkout.zing.work/b/cNi5kE6xO8uvc04fnF5J60L`  →  `price_1U7UnSJdCDYxERimbVLjverh`
- Complete ($189/mo): `https://checkout.zing.work/b/28EcN65tK7qrc042AT5J60M`  →  `price_1U7UnTJdCDYxERimkexpDAHw`

Account: `acct_1MS2Z5JdCDYxERim` (LIVE). If we ever rotate/replace a payment link, update `STRIPE_LINKS` at the top of `onboard-industry-page.py`.
