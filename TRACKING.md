# Tracking & Analytics — Configuration Guide

This site ships with tracking **scaffolding but no live tags**. Every third-party pixel is disabled by default until marketing hands over the IDs and someone updates `/js/tracking.js`.

---

## TL;DR — how to turn on any tag

1. Get the ID from the owner (see table below).
2. Open `/js/tracking.js`, find the `TZ_TRACKING` config block near the top.
3. Paste the ID into the matching field.
4. Commit + push. GitHub Pages redeploys in ~1 min.
5. Verify with the appropriate debugger (Facebook Pixel Helper / GTM Preview / HubSpot Debugger).

**Do not** paste pixels into individual page `<head>` blocks. Everything runs through `tracking.js` so we have one place to audit, one place to disable, and consent gating for free.

---

## What loads where

| File | Purpose |
|---|---|
| `/js/consent.js` | Cookie consent banner + Google Consent Mode v2 defaults. Runs first. Stores choice in `localStorage`. Sets `window.TZ_CONSENT`. |
| `/js/tracking.js` | Reads `TZ_TRACKING` config, loads GTM / GA4 / Facebook Pixel / HubSpot / Google Ads / LinkedIn — but only for categories the visitor has consented to. |
| `/js/forms.js` | DOM event bridge — pushes `form_submit`, `cta_click`, `phone_click`, `email_click`, `outbound_click` events into `dataLayer` so GTM can fire conversion tags. |
| `<script type="application/ld+json">` in each page `<head>` | Structured data (Organization, WebSite, Service, WebPage) for Google Search. Injected by `/tmp/inject_schema.py`. |

All three JS files are `defer`d so they don't block first render.

---

## Tag inventory & owners

| Tag | Config field | Who owns the ID | Notes |
|---|---|---|---|
| **Google Tag Manager** | `gtmContainerId` | Sean (or set up at [tagmanager.google.com](https://tagmanager.google.com)) | **Recommended primary.** Once GTM is installed, add every other tag (GA4, FB Pixel, Google Ads, LinkedIn) inside the GTM UI — no code changes needed for future pixels. |
| **Google Analytics 4** | `ga4MeasurementId` | Sean | Only fill in directly if we're NOT using GTM. If GTM is set, GA4 loads through GTM instead. |
| **Facebook / Meta Pixel** | `facebookPixelId` | Sean / marketing | Only fill in directly if we're NOT using GTM. |
| **HubSpot** | `hubspotPortalId` | Sean | Loads independently (not through GTM — HubSpot docs advise against). Handles tracking, forms, chat, contact-timeline. |
| **Google Ads conversion** | `googleAdsConversionId` | Sean / marketing | Only if not using GTM. |
| **LinkedIn Insight** | `linkedinPartnerId` | Sean / marketing | Only if not using GTM. |

### Recommended setup order

1. **GTM first.** Everything else becomes trivial once GTM exists.
2. **HubSpot second.** Enables forms + chat + contact timeline.
3. Add FB Pixel, GA4, Google Ads, LinkedIn via the **GTM UI** — no repo commits required.

---

## Cookie consent

- Banner appears on first visit; hidden after the visitor makes a choice.
- Three categories: `functional` (always on), `analytics`, `advertising`.
- Choice stored in `localStorage` under `tz_consent_v1`.
- Google Consent Mode v2 is wired up (`ad_storage`, `analytics_storage`, etc.), so Google properties respect the choice even when loaded via GTM.
- Footer "Cookie preferences" link on every page reopens the banner: `window.TZ.openConsent()`.

Programmatic API:

```js
TZ.acceptAll()      // grant analytics + advertising
TZ.rejectAll()      // deny analytics + advertising
TZ.openConsent()    // show the banner again
TZ.getConsent()     // returns { functional, analytics, advertising, timestamp }
```

---

## Form + CTA tracking

`/js/forms.js` auto-fires these `dataLayer` events — no per-form wiring required.

| Event | When it fires | Params |
|---|---|---|
| `form_submit` | Any `<form>` submission | `form_id`, `form_name`, `vertical`, `plan`, `page_path` |
| `cta_click` | Clicks on `.button`, `[data-tz-cta]`, or copy matching "Get Started / Talk to / Choose Local\|Growth\|Complete / Get My…" | `cta_text`, `cta_href`, `vertical`, `plan` |
| `phone_click` | Clicks on `tel:` links | `phone`, `link_text` |
| `email_click` | Clicks on `mailto:` links | `email`, `link_text` |
| `outbound_click` | Clicks on external-origin links | `url`, `link_text` |

To opt a form out: add `data-tz-notrack="1"` to the `<form>` tag.

To fire a custom event from your own code:

```js
TZ.track('inspection_booked', { source: 'chat', vertical: 'roofing' });
```

### HubSpot form embeds

HubSpot forms handle their own conversion tracking, but we also mirror submissions into the `dataLayer` so GTM can see them. When embedding a HubSpot form, use the callback pattern:

```html
<div id="hs-form-contact"></div>
<script>
  hbspt.forms.create({
    portalId: '<PORTAL_ID>',
    formId:   '<FORM_ID>',
    target:   '#hs-form-contact',
    onFormSubmitted: function () {
      TZ.track('form_submit', { form_id: 'hubspot_contact', form_name: 'Contact Us' });
    }
  });
</script>
```

---

## Structured data (SEO)

Every industry page has JSON-LD schema baked into `<head>`:

- `Organization` (TradeZIP) — reused across all pages via `@id` reference
- `WebSite`
- `WebPage`
- `Service` — with `AggregateOffer` covering the three pricing tiers ($79 / $129 / $189)

Blog pages already have `BlogPosting` / `BreadcrumbList` schema from the article generator.

Validate any page with the [Rich Results Test](https://search.google.com/test/rich-results) or [Schema.org validator](https://validator.schema.org/) once we go live.

---

## Post-launch checklist

Once the site is production-ready and pixels are live:

- [ ] Submit `sitemap.xml` to [Google Search Console](https://search.google.com/search-console)
- [ ] Submit `sitemap.xml` to [Bing Webmaster Tools](https://www.bing.com/webmasters)
- [ ] Verify Facebook Pixel with [Meta Pixel Helper](https://chrome.google.com/webstore/detail/meta-pixel-helper/fdgfkebogiimcoedlicjlajpkdmockpc)
- [ ] Verify GTM firing with [Tag Assistant](https://tagassistant.google.com/)
- [ ] Verify HubSpot with [HubSpot Sales Extension debugger](https://chrome.google.com/webstore/detail/hubspot-sales/oiiaigjnkhngdbnoookogelabohpglmd)
- [ ] Enable HTTPS on trade-zip.com (currently `https_enforced: false` — cert mismatch)
- [ ] Run Lighthouse audit — target Performance ≥ 90, SEO ≥ 95
- [ ] Test consent banner on GDPR-region VPN (verify pixels stay off until accept)

---

## Adding a NEW third-party tag later

Best case: it lives inside GTM. Marketing adds it in the GTM UI, no code change, no deploy.

If a new tag can't go through GTM (rare):

1. Add a config field to `TZ_TRACKING` in `/js/tracking.js`.
2. Add a `loadXxx()` function that gates on the appropriate consent category (`hasConsent('analytics')` or `hasConsent('advertising')`).
3. Call it from `loadAll()`.
4. Document it in the "Tag inventory" table above.

Never inline a pixel snippet directly into an HTML page.
