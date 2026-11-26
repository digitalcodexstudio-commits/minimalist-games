// GA4 with Google Consent Mode v2. measurementId mirrors src/js/firebase-config.js.
// Exposes window.mgTrack(eventName, params).
//
// Consent rules:
//  - Do Not Track  -> nothing is loaded.
//  - Storage starts DENIED. It is granted only when
//      a) the Google CMP (TCF API) says GDPR does not apply to the visitor, or
//      b) the visitor gave consent for TCF purpose 1 (store/access information)
//         and purpose 7 (measure ad performance / analytics).
//  - No CMP at all (ad blocker, script failed) -> storage stays denied.
// While denied, GA4 only sends cookieless pings (Consent Mode "advanced").

(function () {
  'use strict';

  var MEASUREMENT_ID = 'G-2VZL4EY33G';

  var dnt = navigator.doNotTrack === '1' || window.doNotTrack === '1';
  var isLocal = /^(localhost|127\.|0\.0\.0\.0)/.test(location.hostname);
  if (dnt || isLocal) {
    window.mgTrack = function () {};
    return;
  }

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  // Must run BEFORE 'config' so the very first hit is already governed by it.
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 800
  });

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
  document.head.appendChild(s);

  gtag('js', new Date());
  gtag('config', MEASUREMENT_ID, { anonymize_ip: true, send_page_view: true });

  window.mgTrack = function (eventName, params) {
    try { gtag('event', eventName, params || {}); } catch (e) {}
  };

  // ---- connect the consent choice to Consent Mode ---------------------------
  var granted = false;
  function grantAnalytics() {
    if (granted) return;
    granted = true;
    gtag('consent', 'update', { analytics_storage: 'granted' });
  }

  // Exposed for tests: decides from a TCData object whether analytics may run.
  function allowedBy(tcData) {
    if (!tcData) return false;
    if (tcData.gdprApplies === false) return true;
    var c = (tcData.purpose && tcData.purpose.consents) || {};
    return c[1] === true && c[7] === true;
  }
  window.__mgConsentAllowedBy = allowedBy;

  function listen() {
    window.__tcfapi('addEventListener', 2, function (tcData, ok) {
      if (!ok || !tcData) return;
      // Only trust final states: a stored choice, or a fresh user action.
      if (tcData.eventStatus === 'tcloaded' || tcData.eventStatus === 'useractioncomplete' ||
          tcData.gdprApplies === false) {
        if (allowedBy(tcData)) grantAnalytics();
      }
    });
  }

  // The CMP is injected by the AdSense script, so it may appear a moment later.
  var tries = 0;
  (function wait() {
    if (typeof window.__tcfapi === 'function') { listen(); return; }
    if (++tries < 40) setTimeout(wait, 250); // give up after ~10 s: stay denied
  })();
})();
