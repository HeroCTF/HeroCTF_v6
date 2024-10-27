const CACHE_NAME = crypto.randomUUID();
const STATIC_FILES = [];

self.addEventListener("install", (event) => {
    console.log("Installing the service worker...");
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_FILES);
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((res) => {
            if (res) {
                console.log(`Loading from the cache: ${event.request.url}.`);
                return res;

            } else {
                console.log(`Fetching ${event.request.url}...`);
                return fetch(event.request).then((res) => {
                    if ((new URL(event.request.url).pathname).startsWith("/c/static/")) {
                        var clonedRes = res.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, new Response(clonedRes.body, { headers: clonedRes.headers }));
                        });
                    }
                    return res;
                });
            }
        })
    );
});

self.addEventListener("activate", (event) => {
    console.log("Activating the service worker...");
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(cacheNames.map((cacheName) => {
                if (!cacheWhitelist.includes(cacheName)) {
                    return caches.delete(cacheName);
                }
            }));
        })
    );
});
