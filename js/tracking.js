/* TradeZIP — third-party tracking loader
 *
 * ONE FILE, ONE PLACE. All third-party pixels/analytics load through here.
 * Every tag is DISABLED by default and gated by TZ_TRACKING config below.
 *
 * ============================================================================
 *  HOW TO ENABLE A TAG (do NOT edit anywhere else)
 * ============================================================================
 *  1. Get the ID from the marketing team (see /TRACKING.md for who owns what).
 *  2. Fill in the matching value in TZ_TRACKING below.
 *  3. Deploy. Verify in browser DevTools + Facebook Pixel Helper /
 *     GTM Preview / HubSpot Debugger.
 *
 *  Nothing fires unless (a) a valid ID is set AND (b) the user has granted
 *  consent for that tag's category. See /js/consent.js for the consent model.
 * ============================================================================
 */

(function () {
  'use strict';

  // ========================================================================
  //  CONFIG — fill these in when marketing hands over the IDs.
  //  Empty string = tag disabled. Do not put fake / placeholder IDs here.
  // ========================================================================
  window.TZ_TRACKING = window.TZ_TRACKING || {
    gtmContainerId:      '',   // e.g. 'GTM-XXXXXXX'   — Google Tag Manager (recommended primary)
    ga4MeasurementId:    '',   // e.g. 'G-XXXXXXXXXX'  — Google Analytics 4 (only if NOT using GTM)
    facebookPixelId:     '',   // e.g. '1234567890'    — Meta / Facebook Pixel (only if NOT using GTM)
    hubspotPortalId:     '',   // e.g. '12345678'      — HubSpot tracking + forms + chat
    googleAdsConversionId: '', // e.g. 'AW-123456789'  — Google Ads (only if NOT using GTM)
    linkedinPartnerId:   '',   // e.g. '1234567'       — LinkedIn Insight Tag (only if NOT using GTM)

    // Environment toggles
    debug:               false,        // set true to console.log every tag firing
    respectDoNotTrack:   true,         // honour browsers with DNT=1
  };

  var cfg = window.TZ_TRACKING;
  var log = cfg.debug ? function () { console.log.apply(console, ['[TZ_TRACKING]'].concat([].slice.call(arguments))); } : function () {};

  // Global dataLayer — required by GTM and used by /js/forms.js for form-submit events.
  // Safe to reference even when no tags are loaded.
  window.dataLayer = window.dataLayer || [];

  // Honour Do-Not-Track header if configured.
  if (cfg.respectDoNotTrack && (navigator.doNotTrack === '1' || window.doNotTrack === '1' || navigator.msDoNotTrack === '1')) {
    log('DNT enabled — no tags will load.');
    return;
  }

  // ========================================================================
  //  CONSENT GATE
  //  Tags only fire once the visitor grants consent for the matching category.
  //  /js/consent.js dispatches 'tz:consent-updated' whenever choices change.
  //  Categories: 'analytics' | 'advertising' | 'functional'
  // ========================================================================
  function hasConsent(category) {
    var c = window.TZ_CONSENT || {};
    return c[category] === true;
  }

  function onConsent(fn) {
    // Fire once now (in case consent was already granted before this script loaded)
    // AND on every future update.
    try { fn(); } catch (e) { console.error('[TZ_TRACKING] consent handler error', e); }
    window.addEventListener('tz:consent-updated', function () {
      try { fn(); } catch (e) { console.error('[TZ_TRACKING] consent handler error', e); }
    });
  }

  // Track which loaders have already fired so consent updates don't re-inject scripts.
  var loaded = { gtm: false, ga4: false, fbq: false, hubspot: false, gads: false, linkedin: false };

  // ========================================================================
  //  1. GOOGLE TAG MANAGER  (primary — manages every other Google/Meta tag from its UI)
  // ========================================================================
  function loadGTM() {
    if (loaded.gtm || !cfg.gtmContainerId) return;
    if (!hasConsent('analytics') && !hasConsent('advertising')) return;
    loaded.gtm = true;
    log('loading GTM', cfg.gtmContainerId);
    (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer',cfg.gtmContainerId);
  }

  // ========================================================================
  //  2. GOOGLE ANALYTICS 4  (only load directly if GTM is NOT installed)
  // ========================================================================
  function loadGA4() {
    if (loaded.ga4 || !cfg.ga4MeasurementId || cfg.gtmContainerId) return;
    if (!hasConsent('analytics')) return;
    loaded.ga4 = true;
    log('loading GA4', cfg.ga4MeasurementId);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(cfg.ga4MeasurementId);
    document.head.appendChild(s);
    window.gtag = window.gtag || function(){dataLayer.push(arguments);};
    gtag('js', new Date());
    gtag('config', cfg.ga4MeasurementId, { anonymize_ip: true });
  }

  // ========================================================================
  //  3. FACEBOOK / META PIXEL  (only load directly if GTM is NOT installed)
  // ========================================================================
  function loadFacebookPixel() {
    if (loaded.fbq || !cfg.facebookPixelId || cfg.gtmContainerId) return;
    if (!hasConsent('advertising')) return;
    loaded.fbq = true;
    log('loading Facebook Pixel', cfg.facebookPixelId);
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', cfg.facebookPixelId);
    fbq('track', 'PageView');
  }

  // ========================================================================
  //  4. HUBSPOT TRACKING  (loads its OWN script — do not put this in GTM per HS docs)
  // ========================================================================
  function loadHubSpot() {
    if (loaded.hubspot || !cfg.hubspotPortalId) return;
    if (!hasConsent('analytics')) return;
    loaded.hubspot = true;
    log('loading HubSpot', cfg.hubspotPortalId);
    var s = document.createElement('script');
    s.id = 'hs-script-loader';
    s.async = true;
    s.defer = true;
    s.src = '//js.hs-scripts.com/' + encodeURIComponent(cfg.hubspotPortalId) + '.js';
    document.body.appendChild(s);
  }

  // ========================================================================
  //  5. GOOGLE ADS CONVERSION TAG  (only load directly if GTM is NOT installed)
  // ========================================================================
  function loadGoogleAds() {
    if (loaded.gads || !cfg.googleAdsConversionId || cfg.gtmContainerId) return;
    if (!hasConsent('advertising')) return;
    loaded.gads = true;
    log('loading Google Ads', cfg.googleAdsConversionId);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(cfg.googleAdsConversionId);
    document.head.appendChild(s);
    window.gtag = window.gtag || function(){dataLayer.push(arguments);};
    gtag('js', new Date());
    gtag('config', cfg.googleAdsConversionId);
  }

  // ========================================================================
  //  6. LINKEDIN INSIGHT TAG  (only load directly if GTM is NOT installed)
  // ========================================================================
  function loadLinkedIn() {
    if (loaded.linkedin || !cfg.linkedinPartnerId || cfg.gtmContainerId) return;
    if (!hasConsent('advertising')) return;
    loaded.linkedin = true;
    log('loading LinkedIn Insight', cfg.linkedinPartnerId);
    window._linkedin_partner_id = cfg.linkedinPartnerId;
    window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
    window._linkedin_data_partner_ids.push(cfg.linkedinPartnerId);
    (function(l){if(!l){window.lintrk=function(a,b){window.lintrk.q.push([a,b])};window.lintrk.q=[]}var s=document.getElementsByTagName('script')[0];var b=document.createElement('script');b.type='text/javascript';b.async=true;b.src='https://snap.licdn.com/li.lms-analytics/insight.min.js';s.parentNode.insertBefore(b,s);})(window.lintrk);
  }

  // ========================================================================
  //  BOOT — wait for consent, then load whatever's configured.
  // ========================================================================
  function loadAll() {
    loadGTM();
    loadGA4();
    loadFacebookPixel();
    loadHubSpot();
    loadGoogleAds();
    loadLinkedIn();
  }

  onConsent(loadAll);

  // ========================================================================
  //  PUBLIC API  — call TZ.track('event_name', { key: value }) from anywhere.
  //  Fires into dataLayer (GTM catches it) AND into fbq if Facebook Pixel is
  //  loaded directly. Use for form submissions, CTA clicks, phone-number clicks.
  // ========================================================================
  window.TZ = window.TZ || {};
  window.TZ.track = function (eventName, params) {
    params = params || {};
    log('event', eventName, params);
    // dataLayer (GTM listens here)
    window.dataLayer.push(Object.assign({ event: eventName }, params));
    // Facebook Pixel direct-load fallback
    if (window.fbq && !cfg.gtmContainerId) {
      try { window.fbq('trackCustom', eventName, params); } catch (e) {}
    }
  };
})();
