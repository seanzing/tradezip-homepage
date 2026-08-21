/* TradeZIP — form + CTA event bridge
 *
 * Auto-wires DOM events into the dataLayer so GTM (and any pixels loaded
 * through it) can fire conversion tags without editing individual forms.
 *
 * Events pushed:
 *   form_submit    — any <form> submission (excluded via data-tz-notrack="1")
 *   cta_click      — clicks on <a>/<button> with class="button" or data-tz-cta
 *   phone_click    — clicks on tel: links
 *   email_click    — clicks on mailto: links
 *   outbound_click — clicks on external links (different origin)
 *
 * For HubSpot form embeds, HubSpot handles its own conversion events, but we
 * also mirror those into the dataLayer via the hbspt.forms.create callback
 * pattern (documented in /TRACKING.md).
 */

(function () {
  'use strict';

  window.dataLayer = window.dataLayer || [];
  function push(eventName, params) {
    var payload = Object.assign({ event: eventName }, params || {});
    window.dataLayer.push(payload);
    if (window.TZ_TRACKING && window.TZ_TRACKING.debug) {
      console.log('[TZ_FORMS]', eventName, payload);
    }
  }

  // -------- Form submissions --------
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.tagName !== 'FORM') return;
    if (form.getAttribute('data-tz-notrack') === '1') return;

    var formId   = form.id || form.getAttribute('name') || 'unnamed_form';
    var formName = form.getAttribute('data-tz-name') || formId;
    var vertical = form.getAttribute('data-vertical') || '';
    var plan     = form.getAttribute('data-plan') || '';

    push('form_submit', {
      form_id:   formId,
      form_name: formName,
      vertical:  vertical || undefined,
      plan:      plan     || undefined,
      page_path: location.pathname,
    });
  }, true);

  // -------- CTA / button clicks + phone/email/outbound --------
  document.addEventListener('click', function (e) {
    var el = e.target;
    // walk up to find <a> or <button> ancestor
    while (el && el !== document.body) {
      if (el.tagName === 'A' || el.tagName === 'BUTTON') break;
      el = el.parentNode;
    }
    if (!el || el === document.body) return;

    var href = (el.getAttribute && el.getAttribute('href')) || '';
    var text = (el.textContent || '').trim().slice(0, 60);
    var cls  = (el.className && el.className.toString) ? el.className.toString() : '';

    // Phone
    if (href.indexOf('tel:') === 0) {
      push('phone_click', { phone: href.replace('tel:', ''), link_text: text });
      return;
    }
    // Email
    if (href.indexOf('mailto:') === 0) {
      push('email_click', { email: href.replace('mailto:', ''), link_text: text });
      return;
    }
    // Primary CTA (button-styled links, explicit data-tz-cta, or "Get Started" / "Talk to" copy)
    var isCta = /\bbutton\b/.test(cls) || el.hasAttribute('data-tz-cta') ||
                /get started|talk to|choose (local|growth|complete)|get my/i.test(text);
    if (isCta) {
      push('cta_click', {
        cta_text: text,
        cta_href: href || undefined,
        vertical: el.getAttribute('data-vertical') || undefined,
        plan:     el.getAttribute('data-plan') || undefined,
      });
    }
    // Outbound (different origin, http/https)
    if (href && /^https?:\/\//i.test(href)) {
      try {
        var u = new URL(href);
        if (u.origin !== location.origin) {
          push('outbound_click', { url: href, link_text: text });
        }
      } catch (err) {}
    }
  }, true);
})();
