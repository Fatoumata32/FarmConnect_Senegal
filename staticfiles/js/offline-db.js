/**
 * Gestion de la base de données IndexedDB pour le mode hors-ligne
 * Permet de stocker les cultures, recommandations, et données météo localement
 */

class FarmConnectDB {
    constructor() {
        this.dbName = 'FarmConnectDB';
        this.version = 1;
        this.db = null;
    }

    /**
     * Initialise la base de données
     */
    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.version);

            request.onerror = () => {
                console.error('Erreur d\'ouverture de la base de données', request.error);
                reject(request.error);
            };

            request.onsuccess = () => {
                this.db = request.result;
                console.log('Base de données ouverte avec succès');
                resolve(this.db);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                console.log('Mise à jour de la base de données...');

                // Store pour les cultures
                if (!db.objectStoreNames.contains('crops')) {
                    const cropsStore = db.createObjectStore('crops', { keyPath: 'id' });
                    cropsStore.createIndex('name_fr', 'name_fr', { unique: false });
                    cropsStore.createIndex('category', 'category', { unique: false });
                    cropsStore.createIndex('growing_season', 'growing_season', { unique: false });
                    console.log('Store "crops" créé');
                }

                // Store pour les types de sol
                if (!db.objectStoreNames.contains('soilTypes')) {
                    const soilStore = db.createObjectStore('soilTypes', { keyPath: 'id' });
                    soilStore.createIndex('name_fr', 'name_fr', { unique: false });
                    console.log('Store "soilTypes" créé');
                }

                // Store pour les recommandations
                if (!db.objectStoreNames.contains('recommendations')) {
                    const recoStore = db.createObjectStore('recommendations', { keyPath: 'id' });
                    recoStore.createIndex('crop_id', 'crop_id', { unique: false });
                    recoStore.createIndex('soil_type_id', 'soil_type_id', { unique: false });
                    console.log('Store "recommendations" créé');
                }

                // Store pour les données météo
                if (!db.objectStoreNames.contains('weather')) {
                    const weatherStore = db.createObjectStore('weather', { keyPath: 'id', autoIncrement: true });
                    weatherStore.createIndex('region', 'region', { unique: false });
                    weatherStore.createIndex('timestamp', 'timestamp', { unique: false });
                    console.log('Store "weather" créé');
                }

                // Store pour les données en attente de synchronisation
                if (!db.objectStoreNames.contains('pendingSync')) {
                    const syncStore = db.createObjectStore('pendingSync', { keyPath: 'id', autoIncrement: true });
                    syncStore.createIndex('timestamp', 'timestamp', { unique: false });
                    console.log('Store "pendingSync" créé');
                }

                // Store pour les favoris de l'utilisateur
                if (!db.objectStoreNames.contains('favorites')) {
                    const favStore = db.createObjectStore('favorites', { keyPath: 'id', autoIncrement: true });
                    favStore.createIndex('crop_id', 'crop_id', { unique: false });
                    favStore.createIndex('user_id', 'user_id', { unique: false });
                    console.log('Store "favorites" créé');
                }

                // Store pour les conseils récents
                if (!db.objectStoreNames.contains('recentTips')) {
                    const tipsStore = db.createObjectStore('recentTips', { keyPath: 'id' });
                    tipsStore.createIndex('crop_id', 'crop_id', { unique: false });
                    tipsStore.createIndex('timestamp', 'timestamp', { unique: false });
                    console.log('Store "recentTips" créé');
                }
            };
        });
    }

    /**
     * Sauvegarde des cultures dans IndexedDB
     */
    async saveCrops(crops) {
        if (!this.db) await this.init();

        const transaction = this.db.transaction(['crops'], 'readwrite');
        const store = transaction.objectStore('crops');

        return Promise.all(
            crops.map(crop => {
                return new Promise((resolve, reject) => {
                    const request = store.put(crop);
                    request.onsuccess = () => resolve(request.result);
                    request.onerror = () => reject(request.error);
                });
            })
        );
    }

    /**
     * Récupère toutes les cultures
     */
    async getAllCrops() {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['crops'], 'readonly');
            const store = transaction.objectStore('crops');
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Récupère une culture par son ID
     */
    async getCropById(id) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['crops'], 'readonly');
            const store = transaction.objectStore('crops');
            const request = store.get(id);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Recherche de cultures par catégorie
     */
    async getCropsByCategory(category) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['crops'], 'readonly');
            const store = transaction.objectStore('crops');
            const index = store.index('category');
            const request = index.getAll(category);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Sauvegarde des types de sol
     */
    async saveSoilTypes(soilTypes) {
        if (!this.db) await this.init();

        const transaction = this.db.transaction(['soilTypes'], 'readwrite');
        const store = transaction.objectStore('soilTypes');

        return Promise.all(
            soilTypes.map(soil => {
                return new Promise((resolve, reject) => {
                    const request = store.put(soil);
                    request.onsuccess = () => resolve(request.result);
                    request.onerror = () => reject(request.error);
                });
            })
        );
    }

    /**
     * Récupère tous les types de sol
     */
    async getAllSoilTypes() {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['soilTypes'], 'readonly');
            const store = transaction.objectStore('soilTypes');
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Sauvegarde des recommandations
     */
    async saveRecommendations(recommendations) {
        if (!this.db) await this.init();

        const transaction = this.db.transaction(['recommendations'], 'readwrite');
        const store = transaction.objectStore('recommendations');

        return Promise.all(
            recommendations.map(reco => {
                return new Promise((resolve, reject) => {
                    const request = store.put(reco);
                    request.onsuccess = () => resolve(request.result);
                    request.onerror = () => reject(request.error);
                });
            })
        );
    }

    /**
     * Récupère les recommandations pour une culture et un type de sol
     */
    async getRecommendations(cropId, soilTypeId) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['recommendations'], 'readonly');
            const store = transaction.objectStore('recommendations');
            const request = store.getAll();

            request.onsuccess = () => {
                const results = request.result.filter(
                    r => r.crop_id === cropId && r.soil_type_id === soilTypeId
                );
                resolve(results);
            };
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Sauvegarde les données météo
     */
    async saveWeather(weatherData) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['weather'], 'readwrite');
            const store = transaction.objectStore('weather');

            // Ajouter un timestamp
            weatherData.timestamp = Date.now();

            const request = store.add(weatherData);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Récupère les données météo pour une région
     */
    async getWeatherByRegion(region) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['weather'], 'readonly');
            const store = transaction.objectStore('weather');
            const index = store.index('region');
            const request = index.getAll(region);

            request.onsuccess = () => {
                // Retourner les données les plus récentes
                const results = request.result.sort((a, b) => b.timestamp - a.timestamp);
                resolve(results[0] || null);
            };
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Ajoute une culture aux favoris
     */
    async addToFavorites(cropId, userId) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['favorites'], 'readwrite');
            const store = transaction.objectStore('favorites');

            const favorite = {
                crop_id: cropId,
                user_id: userId,
                timestamp: Date.now()
            };

            const request = store.add(favorite);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Récupère les cultures favorites d'un utilisateur
     */
    async getFavorites(userId) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['favorites'], 'readonly');
            const store = transaction.objectStore('favorites');
            const index = store.index('user_id');
            const request = index.getAll(userId);

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Ajoute des données en attente de synchronisation
     */
    async addPendingSync(data) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['pendingSync'], 'readwrite');
            const store = transaction.objectStore('pendingSync');

            data.timestamp = Date.now();
            data.synced = false;

            const request = store.add(data);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Récupère toutes les données en attente de synchronisation
     */
    async getPendingSync() {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['pendingSync'], 'readonly');
            const store = transaction.objectStore('pendingSync');
            const request = store.getAll();

            request.onsuccess = () => {
                const pending = request.result.filter(item => !item.synced);
                resolve(pending);
            };
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Marque une donnée comme synchronisée
     */
    async markAsSynced(id) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['pendingSync'], 'readwrite');
            const store = transaction.objectStore('pendingSync');
            const request = store.delete(id);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Nettoie les anciennes données météo (> 24h)
     */
    async cleanOldWeather() {
        if (!this.db) await this.init();

        const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction(['weather'], 'readwrite');
            const store = transaction.objectStore('weather');
            const index = store.index('timestamp');
            const range = IDBKeyRange.upperBound(oneDayAgo);
            const request = index.openCursor(range);

            request.onsuccess = (event) => {
                const cursor = event.target.result;
                if (cursor) {
                    cursor.delete();
                    cursor.continue();
                } else {
                    resolve();
                }
            };

            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Obtient la taille de la base de données
     */
    async getDatabaseSize() {
        if (!this.db) await this.init();

        const stores = ['crops', 'soilTypes', 'recommendations', 'weather', 'pendingSync', 'favorites', 'recentTips'];
        let totalSize = 0;

        for (const storeName of stores) {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const count = await new Promise((resolve, reject) => {
                const request = store.count();
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            });

            totalSize += count;
        }

        return {
            stores: stores.length,
            totalRecords: totalSize,
            details: {
                crops: await this.getStoreCount('crops'),
                soilTypes: await this.getStoreCount('soilTypes'),
                recommendations: await this.getStoreCount('recommendations'),
                weather: await this.getStoreCount('weather'),
                pendingSync: await this.getStoreCount('pendingSync'),
                favorites: await this.getStoreCount('favorites'),
                recentTips: await this.getStoreCount('recentTips')
            }
        };
    }

    /**
     * Compte les enregistrements dans un store
     */
    async getStoreCount(storeName) {
        if (!this.db) await this.init();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.count();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Vide complètement la base de données
     */
    async clearAll() {
        if (!this.db) await this.init();

        const stores = ['crops', 'soilTypes', 'recommendations', 'weather', 'pendingSync', 'favorites', 'recentTips'];

        return Promise.all(
            stores.map(storeName => {
                return new Promise((resolve, reject) => {
                    const transaction = this.db.transaction([storeName], 'readwrite');
                    const store = transaction.objectStore(storeName);
                    const request = store.clear();

                    request.onsuccess = () => resolve();
                    request.onerror = () => reject(request.error);
                });
            })
        );
    }
}

// Instance globale
const farmConnectDB = new FarmConnectDB();

// Initialisation au chargement de la page
if (typeof window !== 'undefined') {
    window.farmConnectDB = farmConnectDB;

    // Auto-initialisation
    farmConnectDB.init().catch(err => {
        console.error('Erreur d\'initialisation de la base de données:', err);
    });
}

console.log('[IndexedDB] Script chargé');
