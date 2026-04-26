// Service worker for offline play.
// HTML: network-first (so updates ship without a hard refresh).
// Static assets: cache-first.

const VERSION = 'v6';
const STATIC_CACHE = 'mg-static-' + VERSION;
const RUNTIME_CACHE = 'mg-runtime-' + VERSION;

const PRECACHE_URLS = [
  '/',
  '/games/sudoku',
  '/games/minesweeper',
  '/games/2048',
  '/blog',
  '/src/css/global.css',
  '/src/css/responsive.css',
  '/src/css/games.css',
  '/src/css/blog.css',
  '/src/js/app.js',
  '/public/favicon.svg',
  '/manifest.webmanifest'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => cache.addAll(PRECACHE_URLS).catch(() => {}))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((k) => k !== STATIC_CACHE && k !== RUNTIME_CACHE).map((k) => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== location.origin) return;

  const isHTML = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').includes('text/html');

  if (isHTML) {
    event.respondWith(networkFirst(req));
  } else {
    event.respondWith(cacheFirst(req));
  }
});

function networkFirst(req) {
  return fetch(req)
    .then((res) => {
      const copy = res.clone();
      caches.open(RUNTIME_CACHE).then((c) => c.put(req, copy));
      return res;
    })
    .catch(() => caches.match(req).then((cached) => cached || caches.match('/')));
}

function cacheFirst(req) {
  return caches.match(req).then((cached) => {
    if (cached) return cached;
    return fetch(req).then((res) => {
      if (res.ok) {
        const copy = res.clone();
        caches.open(RUNTIME_CACHE).then((c) => c.put(req, copy));
      }
      return res;
    });
  });
}
