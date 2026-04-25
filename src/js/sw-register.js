// Register service worker post-load to keep it off the critical path.
// Skips localhost so emulator development doesn't get a stale cache.

(function () {
  'use strict';
  if (!('serviceWorker' in navigator)) return;
  if (/^(localhost|127\.|0\.0\.0\.0)/.test(location.hostname)) return;

  window.addEventListener('load', function () {
    navigator.serviceWorker.register('/service-worker.js').catch(function () {});
  });
})();
