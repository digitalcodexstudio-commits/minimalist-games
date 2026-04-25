// GA4 setup. measurementId mirrors src/js/firebase-config.js.
// Respects Do Not Track. Exposes window.mgTrack(eventName, params).

(function () {
  'use strict';

  var MEASUREMENT_ID = 'G-2VZL4EY33G';

  // Honour Do Not Track and skip on localhost so dev sessions don't pollute data.
  var dnt = navigator.doNotTrack === '1' || window.doNotTrack === '1';
  var isLocal = /^(localhost|127\.|0\.0\.0\.0)/.test(location.hostname);
  if (dnt || isLocal) {
    window.mgTrack = function () {};
    return;
  }

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', MEASUREMENT_ID, {
    anonymize_ip: true,
    send_page_view: true
  });

  window.mgTrack = function (eventName, params) {
    try { gtag('event', eventName, params || {}); } catch (e) {}
  };
})();
