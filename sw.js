/* Daily Spend service worker: keeps the app's own files on the device so it opens offline.
   It only ever answers requests for files of this site, and never sends anything anywhere.

   Releasing a new version: change VERSION here (and STRINGS.version in app.js). Because files
   are served cache-first, a change is only picked up through a new VERSION. */
const VERSION = '0.2.0';
const CACHE = 'ds-' + VERSION;
const ASSETS = [
  './',
  'index.html',
  'styles.css',
  'app.js',
  'manifest.webmanifest',
  'data/cards-ca.json',
  'icons/icon-192.png',
  'icons/icon-512.png',
  'icons/icon-maskable-512.png',
  'icons/apple-touch-icon.png'
];

self.addEventListener('install', (event) => {
  // cache: 'reload' skips the browser's HTTP cache, so a new version never stores stale files.
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ASSETS.map((url) => new Request(url, { cache: 'reload' }))))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key.indexOf('ds-') === 0 && key !== CACHE).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

// The page's "Update ready · Reload" banner sends this to let a waiting version take over.
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  if (new URL(request.url).origin !== self.location.origin) return;
  event.respondWith(
    caches.open(CACHE).then((cache) =>
      cache.match(request, { ignoreSearch: true }).then((hit) => hit || fetch(request).catch((err) => {
        // Offline and not one of the app's files: a page load still gets the app.
        if (request.mode !== 'navigate') throw err;
        return cache.match('./').then((page) => page || Promise.reject(err));
      })))
  );
});
