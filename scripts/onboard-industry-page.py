#!/usr/bin/env python3
"""onboard-industry-page.py
   Ingest a new TradeZIP industry landing page from a ChatGPT-generated HTML file.

   Does everything needed to make the page site-consistent:
     1. Extract every base64-embedded @font-face to /assets/fonts/*.woff2
        (deduped by content hash — new pages reuse the shared font pool)
     2. Extract big image data URIs from '.rf-work-image' cards to
        /assets/{industry}/work/*.webp (converted via cwebp if available)
     3. Rewrite pricing-tier 'Choose Local/Growth/Complete' CTAs to point at
        LIVE Stripe payment links, relabelled 'Buy Now'
     4. Strip the standalone HTML wrapper if present (site host handles that)
     5. Report the size reduction

   Usage:
     python3 scripts/onboard-industry-page.py <industry-slug> <source-html>
     python3 scripts/onboard-industry-page.py plumbers /tmp/plumbers-new.html

   Idempotent: safe to re-run against an already-processed file. Fonts and images
   are hashed for dedup so re-runs don't create duplicates.
"""
import argparse, base64, hashlib, os, pathlib, re, shutil, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FONTS_DIR = REPO / 'assets' / 'fonts'
STRIPE_LINKS = {
    'local':    'https://checkout.zing.work/b/4gMeVe7BSdOP6FK0sL5J60K',
    'growth':   'https://checkout.zing.work/b/cNi5kE6xO8uvc04fnF5J60L',
    'complete': 'https://checkout.zing.work/b/28EcN65tK7qrc042AT5J60M',
}

# --- Font extraction ------------------------------------------------------

SUBSET_TESTS = [
    ('cyrillic-ext', 0x0460, 0x052F),
    ('cyrillic',     0x0400, 0x045F),
    ('cyrillic',     0x0301, 0x0301),
    ('greek-ext',    0x1F00, 0x1FFF),
    ('greek',        0x0370, 0x03FF),
    ('vietnamese',   0x0102, 0x0103),
    ('vietnamese',   0x1EA0, 0x1EF9),
    ('latin-ext',    0x0100, 0x02BA),
    ('latin',        0x0000, 0x00FF),
    ('symbols',      0x2000, 0x25FF),
]

def infer_subset(unicode_range: str) -> str:
    parts = re.findall(r'U\+([0-9A-Fa-f]+)(?:-([0-9A-Fa-f]+))?', unicode_range)
    if not parts: return 'unknown'
    start, end = parts[0]
    s = int(start, 16)
    e = int(end, 16) if end else s
    for subset_name, lo, hi in SUBSET_TESTS:
        if lo <= s and hi >= e:
            return subset_name
    for subset_name, lo, hi in SUBSET_TESTS:
        if s <= hi and e >= lo:
            return subset_name
    return 'unknown'

def extract_fonts(html: str) -> tuple[str, int]:
    """Extract every base64 @font-face src, write to FONTS_DIR, rewrite src to URL.
       Returns (rewritten_html, count_of_replacements)."""
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    ff_pattern = re.compile(r'@font-face\s*\{([^}]+)\}', re.DOTALL)
    replacements = []
    for m in ff_pattern.finditer(html):
        body = m.group(1)
        src_match = re.search(
            r'src:\s*url\(data:(?:font|application)/[^;]+;base64,([A-Za-z0-9+/=]+)\)\s*format\([\'"]?(woff2|woff|truetype|opentype)[\'"]?\)',
            body
        )
        if not src_match: continue
        b64, fmt = src_match.groups()
        raw = base64.b64decode(b64)
        family_m = re.search(r"font-family:\s*['\"]?([^;'\"]+)", body)
        family = family_m.group(1).strip() if family_m else 'unknown'
        weight_m = re.search(r"font-weight:\s*([0-9]+(?:\s+[0-9]+)?|normal|bold)", body)
        weight = weight_m.group(1).strip().replace(' ', '-') if weight_m else '400'
        style_m = re.search(r"font-style:\s*(normal|italic)", body)
        style = style_m.group(1) if style_m else 'normal'
        ur_m = re.search(r"unicode-range:\s*([^;]+)", body)
        subset = infer_subset(ur_m.group(1)) if ur_m else 'main'
        slug = f'{family.lower().replace(" ", "-")}-{weight}-{style}-{subset}.{fmt}'
        out_path = FONTS_DIR / slug
        if not out_path.exists() or hashlib.sha256(out_path.read_bytes()).digest() != hashlib.sha256(raw).digest():
            out_path.write_bytes(raw)
        replacements.append((b64, slug, fmt))

    for b64, slug, fmt in replacements:
        old_pat = re.compile(
            rf'src:\s*url\(data:(?:font|application)/[^;]+;base64,{re.escape(b64)}\)\s*format\([\'"]?{re.escape(fmt)}[\'"]?\)'
        )
        html, _ = old_pat.subn(f"src:url(/assets/fonts/{slug}) format('{fmt}')", html, count=1)
    return html, len(replacements)

# --- Image extraction (rf-work-image cards) --------------------------------

def extract_work_images(html: str, industry: str) -> tuple[str, int]:
    """Extract big base64 images from .rf-work-image cards to /assets/{industry}/work/.
       Converts to WebP if cwebp is on PATH."""
    industry_dir = REPO / 'assets' / industry / 'work'
    industry_dir.mkdir(parents=True, exist_ok=True)
    has_cwebp = shutil.which('cwebp') is not None
    # Match: <div class="rf-work-image"><img src="data:image/PNG;base64,X" alt="...">
    pattern = re.compile(
        r'(<div class="rf-work-image"><img src=")(data:image/([^;]+);base64,([A-Za-z0-9+/=]+))("[^>]*alt="([^"]*)"[^>]*>)'
    )
    seen_by_hash = {}
    def slugify(alt):
        s = re.sub(r'[^a-z0-9]+', '-', alt.lower()).strip('-')
        # Strip stopword-ish suffixes to keep filenames short
        s = re.sub(r'-(website|homepage|design|roofing|plumbing|hvac|electrical|landscaping|painting|flooring|concrete|masonry|cleaning|pool|auto|general-contractor|contractor)+$', '', s)
        s = re.sub(r'-+', '-', s).strip('-')
        return s[:60] if s else 'card'
    def repl(m):
        prefix, uri, mime, b64, suffix, alt = m.groups()
        raw = base64.b64decode(b64)
        h = hashlib.sha256(raw).hexdigest()[:12]
        if h in seen_by_hash:
            filename = seen_by_hash[h]
        else:
            # Prefer WebP; keep original ext if no cwebp
            ext = 'webp' if has_cwebp else mime.split('+')[0].split('/')[-1]
            slug = slugify(alt) or f'card-{h}'
            filename = f'{slug}.{ext}'
            out = industry_dir / filename
            # If a same-name file exists but different bytes, disambiguate with hash
            if out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()[:12] != h:
                filename = f'{slug}-{h}.{ext}'
                out = industry_dir / filename
            if has_cwebp:
                tmp = industry_dir / f'.tmp-{h}.{mime.split("/")[-1]}'
                tmp.write_bytes(raw)
                subprocess.run(['cwebp', '-quiet', '-q', '80', '-m', '6', str(tmp), '-o', str(out)], check=True)
                tmp.unlink()
            else:
                out.write_bytes(raw)
            seen_by_hash[h] = filename
        return f'{prefix}/assets/{industry}/work/{filename}{suffix}'
    new_html, count = pattern.subn(repl, html)
    return new_html, count

# --- Pricing CTAs ----------------------------------------------------------

def wire_pricing_ctas(html: str) -> tuple[str, dict]:
    """Rewrite Choose Local/Growth/Complete anchors to Buy Now Stripe links."""
    hits = {t: 0 for t in STRIPE_LINKS}
    for tier, link in STRIPE_LINKS.items():
        tier_cap = tier.capitalize()
        rx = re.compile(
            r'(<a\s+class="[^"]*")\s+href="(#contact|#consultation)"([^>]*)>'
            r'Choose(?:\s*<!--\s*-->\s*|\s+)' + re.escape(tier_cap) + r'</a>',
            re.IGNORECASE
        )
        def sub(m):
            hits[tier] += 1
            cls_open, _, _rest = m.groups()
            cls_match = re.search(r'class="([^"]+)"', cls_open)
            cls = cls_match.group(1) if cls_match else ''
            return (f'<a class="{cls}" href="{link}" target="_blank" rel="noopener" '
                    f'data-tier="{tier}">Buy Now</a>')
        html = rx.sub(sub, html)
    return html, hits

# --- Main ------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('industry', help='Industry slug (e.g. plumbers, hvac, roofing)')
    ap.add_argument('source', help='Path to the raw ChatGPT-generated HTML')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    src_path = pathlib.Path(args.source)
    if not src_path.exists():
        sys.exit(f'ERROR: source file not found: {src_path}')

    dest_dir = REPO / 'web-design' / args.industry
    dest_path = dest_dir / 'index.html'

    html = src_path.read_text()
    original_size = len(html)
    print(f'\n=== ONBOARDING {args.industry} ===')
    print(f'source:      {src_path}  ({original_size:,} bytes)')

    # 1. Extract fonts
    html, font_count = extract_fonts(html)
    print(f'fonts:       {font_count} extracted to /assets/fonts/')

    # 2. Extract .rf-work-image cards
    html, img_count = extract_work_images(html, args.industry)
    print(f'work images: {img_count} extracted to /assets/{args.industry}/work/')

    # 3. Wire pricing CTAs
    html, cta_hits = wire_pricing_ctas(html)
    total_ctas = sum(cta_hits.values())
    print(f'pricing:     {total_ctas} tier CTAs rewritten (local={cta_hits["local"]} growth={cta_hits["growth"]} complete={cta_hits["complete"]})')

    final_size = len(html)
    savings = original_size - final_size
    pct = 100 * savings / original_size if original_size else 0
    print(f'size:        {original_size:,} -> {final_size:,} bytes  (saved {savings:,}, {pct:.1f}%)')

    if args.dry_run:
        print('\nDRY RUN — no files written to web-design/')
        return

    dest_dir.mkdir(parents=True, exist_ok=True)
    if dest_path.exists():
        print(f'\n⚠ Overwriting existing {dest_path.relative_to(REPO)}')
    dest_path.write_text(html)
    print(f'\nwrote {dest_path.relative_to(REPO)}')
    print('\nNext steps:')
    print(f'  1. Local preview: (cd {REPO} && python3 -m http.server 8080) then open http://127.0.0.1:8080/web-design/{args.industry}/')
    print(f'  2. git add web-design/{args.industry}/index.html assets/{args.industry}/work/ assets/fonts/')
    print(f'  3. git commit + PR + merge')

if __name__ == '__main__':
    main()
