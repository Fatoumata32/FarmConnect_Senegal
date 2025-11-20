/**
 * Service Worker pour FarmConnect Senegal
 * Permet le fonctionnement hors-ligne de l'application
 */

const CACHE_NAME = 'farmconnect-v1';
const OFFLINE_URL = '/offline.html';

// Ressources à mettre en cache immédiatement
const STATIC_ASSETS = [
    '/',
    '/static/css/farmconnect.css',
    '/static/img/FarmConnect_square.png',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
];

// Installation du Service Worker
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installation...');

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[Service Worker] Mise en cache des ressources statiques');
                return cache.addAll(STATIC_ASSETS.map(url => new Request(url, {cache: 'no-cache'})));
            })
            .catch((error) => {
                console.error('[Service Worker] Erreur lors de la mise en cache:', error);
            })
    );

    // Force le nouveau Service Worker à prendre le contrôle immédiatement
    self.skipWaiting();
});

// Activation du Service Worker
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activation...');

    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Suppression ancien cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );

    // Prend le contrôle de toutes les pages immédiatement
    return self.clients.claim();
});

// Stratégie de gestion des requêtes
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Ignorer les requêtes non-HTTP/HTTPS
    if (!request.url.startsWith('http')) {
        return;
    }

    // Stratégie différente selon le type de ressource
    if (request.method === 'GET') {
        // Pour les API - Network First, puis Cache
        if (url.pathname.startsWith('/api/')) {
            event.respondWith(networkFirstStrategy(request));
        }
        // Pour les pages HTML - Network First avec timeout
        else if (request.headers.get('accept').includes('text/html')) {
            event.respondWith(htmlNetworkFirstStrategy(request));
        }
        // Pour les ressources statiques - Cache First
        else if (request.url.includes('/static/') ||
                 request.url.includes('bootstrap') ||
                 request.url.includes('fontawesome') ||
                 request.url.includes('cdnjs')) {
            event.respondWith(cacheFirstStrategy(request));
        }
        // Pour les images
        else if (request.headers.get('accept').includes('image')) {
            event.respondWith(cacheFirstStrategy(request));
        }
        // Par défaut - Network First
        else {
            event.respondWith(networkFirstStrategy(request));
        }
    }
});

/**
 * Stratégie Cache First: Cherche d'abord dans le cache, puis sur le réseau
 */
async function cacheFirstStrategy(request) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);

    if (cachedResponse) {
        // console.log('[Service Worker] Récupération depuis le cache:', request.url);
        return cachedResponse;
    }

    try {
        const networkResponse = await fetch(request);

        // Mise en cache de la réponse si elle est valide
        if (networkResponse && networkResponse.status === 200) {
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.error('[Service Worker] Erreur réseau:', error);

        // Si image, retourner une image placeholder
        if (request.headers.get('accept').includes('image')) {
            return new Response(
                '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect fill="#ddd" width="200" height="200"/><text x="50%" y="50%" text-anchor="middle" fill="#999" font-size="16">Image non disponible</text></svg>',
                { headers: { 'Content-Type': 'image/svg+xml' } }
            );
        }

        throw error;
    }
}

/**
 * Stratégie Network First: Cherche d'abord sur le réseau, puis dans le cache
 */
async function networkFirstStrategy(request) {
    const cache = await caches.open(CACHE_NAME);

    try {
        const networkResponse = await fetch(request);

        // Mise en cache de la réponse si elle est valide
        if (networkResponse && networkResponse.status === 200) {
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.log('[Service Worker] Mode hors-ligne, utilisation du cache');
        const cachedResponse = await cache.match(request);

        if (cachedResponse) {
            return cachedResponse;
        }

        throw error;
    }
}

/**
 * Stratégie Network First pour HTML avec timeout rapide
 */
async function htmlNetworkFirstStrategy(request) {
    const cache = await caches.open(CACHE_NAME);

    try {
        // Timeout de 3 secondes pour le réseau
        const networkResponse = await Promise.race([
            fetch(request),
            new Promise((_, reject) =>
                setTimeout(() => reject(new Error('timeout')), 3000)
            )
        ]);

        if (networkResponse && networkResponse.status === 200) {
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.log('[Service Worker] Timeout ou erreur réseau, utilisation du cache');

        const cachedResponse = await cache.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }

        // Page offline si rien dans le cache
        const offlinePage = await cache.match(OFFLINE_URL);
        if (offlinePage) {
            return offlinePage;
        }

        // Réponse offline basique
        return new Response(
            '<html><body><h1>Mode hors-ligne</h1><p>Vous êtes actuellement hors-ligne. Veuillez vérifier votre connexion internet.</p></body></html>',
            { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
        );
    }
}

/**
 * Écoute des messages depuis la page
 */
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data && event.data.type === 'CACHE_URLS') {
        const urlsToCache = event.data.urls;
        caches.open(CACHE_NAME).then((cache) => {
            cache.addAll(urlsToCache);
        });
    }
});

/**
 * Background Sync - Synchronisation en arrière-plan
 */
self.addEventListener('sync', (event) => {
    console.log('[Service Worker] Background sync:', event.tag);

    if (event.tag === 'sync-data') {
        event.waitUntil(syncData());
    }
});

async function syncData() {
    try {
        // Récupérer les données à synchroniser depuis IndexedDB
        const db = await openDatabase();
        const pendingData = await getPendingData(db);

        // Envoyer les données au serveur
        for (const data of pendingData) {
            try {
                const response = await fetch('/api/sync/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    // Supprimer les données synchronisées
                    await removePendingData(db, data.id);
                }
            } catch (error) {
                console.error('[Service Worker] Erreur de synchronisation:', error);
            }
        }

        console.log('[Service Worker] Synchronisation terminée');
    } catch (error) {
        console.error('[Service Worker] Erreur lors de la synchronisation:', error);
    }
}

// Helpers pour IndexedDB
function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('FarmConnectDB', 1);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

function getPendingData(db) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['pendingSync'], 'readonly');
        const store = transaction.objectStore('pendingSync');
        const request = store.getAll();

        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

function removePendingData(db, id) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['pendingSync'], 'readwrite');
        const store = transaction.objectStore('pendingSync');
        const request = store.delete(id);

        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
    });
}

console.log('[Service Worker] Script chargé');
