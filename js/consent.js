/* TradeZIP — cookie consent banner
 *
 * Minimal, self-hosted, zero-dependency GDPR / CCPA-compatible banner.
 * Stores the visitor's choices in localStorage and exposes window.TZ_CONSENT
 * so /js/tracking.js knows what tags are allowed to fire.
 *
 * Categories:
 *   functional  — always granted, needed for the site to work
 *   analytics   — GA4, HubSpot analytics, GTM analytics tags
 *   advertising — Facebook Pixel, Google Ads conversion, LinkedIn Insight
 *
 * Google Consent Mode v2:
 *   We also call gtag('consent', 'update', ...) so Google tools respect the
 *   visitor's choice even when loaded through GTM.
 */

(function () {
  'use strict';

  var STORAGE_KEY = 'tz_consent_v1';
  var CATEGORIES = ['functional', 'analytics', 'advertising'];

  // Load prior choice from localStorage
  var stored = null;
  try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'); } catch (e) {}

  // Set defaults BEFORE anything else runs. Deny everything except functional
  // until the user explicitly grants consent (safer default, GDPR-aligned).
  window.TZ_CONSENT = stored || {
    functional: true,
    analytics: false,
    advertising: false,
    timestamp: null,
  };

  // Google Consent Mode v2 default (before gtag loads).
  // GTM/GA4 will pick this up automatically when they initialise.
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag('consent', 'default', {
    ad_storage:          window.TZ_CONSENT.advertising ? 'granted' : 'denied',
    ad_user_data:        window.TZ_CONSENT.advertising ? 'granted' : 'denied',
    ad_personalization:  window.TZ_CONSENT.advertising ? 'granted' : 'denied',
    analytics_storage:   window.TZ_CONSENT.analytics   ? 'granted' : 'denied',
    functionality_storage: 'granted',
    security_storage:      'granted',
    wait_for_update: 500,
  });

  function saveConsent(choices) {
    var payload = {
      functional:  true,
      analytics:   choices.analytics === true,
      advertising: choices.advertising === true,
      timestamp:   new Date().toISOString(),
    };
    window.TZ_CONSENT = payload;
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(payload)); } catch (e) {}

    // Update Google Consent Mode v2
    gtag('consent', 'update', {
      ad_storage:         payload.advertising ? 'granted' : 'denied',
      ad_user_data:       payload.advertising ? 'granted' : 'denied',
      ad_personalization: payload.advertising ? 'granted' : 'denied',
      analytics_storage:  payload.analytics   ? 'granted' : 'denied',
    });

    // Broadcast — /js/tracking.js listens for this and will lazy-load any
    // tags whose consent has just been granted.
    window.dispatchEvent(new CustomEvent('tz:consent-updated', { detail: payload }));
  }

  // Re-open button (footer link etc.) — call TZ.openConsent() to show the banner again.
  window.TZ = window.TZ || {};
  window.TZ.openConsent = function () { showBanner(); };
  window.TZ.acceptAll   = function () { saveConsent({ analytics: true,  advertising: true  }); hideBanner(); };
  window.TZ.rejectAll   = function () { saveConsent({ analytics: false, advertising: false }); hideBanner(); };
  window.TZ.getConsent  = function () { return Object.assign({}, window.TZ_CONSENT); };

  // ------------------------------------------------------------------
  //  Banner UI — inline styles so it works even before CSS loads.
  // ------------------------------------------------------------------
  var bannerEl = null;

  function buildBanner() {
    if (bannerEl) return bannerEl;
    bannerEl = document.createElement('div');
    bannerEl.id = 'tz-consent-banner';
    bannerEl.setAttribute('role', 'dialog');
    bannerEl.setAttribute('aria-label', 'Cookie consent');
    bannerEl.setAttribute('aria-live', 'polite');
    bannerEl.style.cssText = [
      'position:fixed', 'bottom:16px', 'left:16px', 'right:16px',
      'max-width:1100px', 'margin:0 auto',
      'background:#050536', 'color:#fff',
      'border:1px solid rgba(255,255,255,0.15)', 'border-radius:16px',
      'box-shadow:0 20px 60px rgba(0,0,0,0.5)',
      'padding:20px 22px', 'z-index:99999',
      'font-family:"Avenir Next", "Helvetica Neue", Arial, sans-serif',
      'font-size:14px', 'line-height:1.5'
    ].join(';');

    bannerEl.innerHTML = '' +
      '<div style="display:flex;gap:22px;align-items:center;flex-wrap:wrap;justify-content:space-between">' +
      '  <div style="flex:1 1 340px;min-width:280px">' +
      '    <strong style="display:block;font-size:15px;margin-bottom:6px">We use cookies to improve your experience</strong>' +
      '    <span style="color:#bdc6e0">Analytics cookies help us understand how visitors use trade-zip.com. Advertising cookies help us measure and improve our marketing. You can accept all, reject non-essential, or customize below. See our <a href="/privacy/" style="color:#34e1d2;text-decoration:underline">Privacy Policy</a>.</span>' +
      '  </div>' +
      '  <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;align-items:center">' +
      '    <button type="button" data-tz-consent="customize" style="background:transparent;border:1px solid rgba(255,255,255,0.35);color:#fff;padding:10px 16px;border-radius:10px;font-weight:600;cursor:pointer;font:inherit">Customize</button>' +
      '    <button type="button" data-tz-consent="reject" style="background:transparent;border:1px solid rgba(255,255,255,0.35);color:#fff;padding:10px 16px;border-radius:10px;font-weight:600;cursor:pointer;font:inherit">Reject non-essential</button>' +
      '    <button type="button" data-tz-consent="accept" style="background:linear-gradient(135deg,#34e1d2 0%,#00aeff 32%,#3a5aff 64%,#9600ff 100%);color:#fff;border:0;padding:10px 20px;border-radius:10px;font-weight:700;cursor:pointer;font:inherit">Accept all</button>' +
      '  </div>' +
      '</div>' +
      '<div id="tz-consent-detail" style="display:none;margin-top:18px;padding-top:18px;border-top:1px solid rgba(255,255,255,0.15)">' +
      '  <label style="display:flex;gap:12px;align-items:flex-start;margin-bottom:10px;cursor:not-allowed;opacity:0.6">' +
      '    <input type="checkbox" checked disabled style="margin-top:3px">' +
      '    <span><strong>Functional</strong> — required for the site to work. Always on.</span>' +
      '  </label>' +
      '  <label style="display:flex;gap:12px;align-items:flex-start;margin-bottom:10px;cursor:pointer">' +
      '    <input type="checkbox" data-tz-cat="analytics" style="margin-top:3px">' +
      '    <span><strong>Analytics</strong> — helps us understand how visitors use the site (Google Analytics, HubSpot).</span>' +
      '  </label>' +
      '  <label style="display:flex;gap:12px;align-items:flex-start;margin-bottom:14px;cursor:pointer">' +
      '    <input type="checkbox" data-tz-cat="advertising" style="margin-top:3px">' +
      '    <span><strong>Advertising</strong> — lets us measure marketing performance and show relevant ads (Facebook Pixel, Google Ads, LinkedIn).</span>' +
      '  </label>' +
      '  <button type="button" data-tz-consent="save" style="background:linear-gradient(135deg,#34e1d2 0%,#00aeff 32%,#3a5aff 64%,#9600ff 100%);color:#fff;border:0;padding:10px 20px;border-radius:10px;font-weight:700;cursor:pointer;font:inherit">Save preferences</button>' +
      '</div>';

    bannerEl.addEventListener('click', function (e) {
      var action = e.target && e.target.getAttribute && e.target.getAttribute('data-tz-consent');
      if (!action) return;
      if (action === 'accept')    { window.TZ.acceptAll(); }
      if (action === 'reject')    { window.TZ.rejectAll(); }
      if (action === 'customize') {
        var d = bannerEl.querySelector('#tz-consent-detail');
        if (d) d.style.display = d.style.display === 'none' ? 'block' : 'none';
      }
      if (action === 'save') {
        var choices = {};
        bannerEl.querySelectorAll('input[data-tz-cat]').forEach(function (cb) {
          choices[cb.getAttribute('data-tz-cat')] = cb.checked;
        });
        saveConsent(choices);
        hideBanner();
      }
    });

    return bannerEl;
  }

  function showBanner() {
    var el = buildBanner();
    if (!el.parentNode) document.body.appendChild(el);
    el.style.display = 'block';
  }

  function hideBanner() {
    if (bannerEl) bannerEl.style.display = 'none';
  }

  // Show the banner only if the visitor hasn't chosen yet.
  function boot() {
    if (!stored) {
      // Wait for body if DOM not ready
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', showBanner);
      } else {
        showBanner();
      }
    }
  }
  boot();
})();
