/**
 * Script de synchronisation des données entre le serveur et IndexedDB
 * Permet de maintenir les données à jour et de gérer le mode hors-ligne
 */

class DataSync {
    constructor() {
        this.isOnline = navigator.onLine;
        this.isSyncing = false;
        this.lastSyncTime = null;

        this.init();
    }

    /**
     * Initialisation des event listeners
     */
    init() {
        // Écoute des changements de connexion
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());

        // Synchronisation périodique toutes les 30 minutes
        setInterval(() => {
            if (this.isOnline) {
                this.syncAll();
            }
        }, 30 * 60 * 1000);

        // Synchronisation au chargement de la page
        if (this.isOnline) {
            this.syncAll();
        }

        // Mise à jour de l'indicateur de statut
        this.updateConnectionStatus();

        console.log('[Data Sync] Initialisation terminée');
    }

    /**
     * Gestion du passage en ligne
     */
    handleOnline() {
        console.log('[Data Sync] Connexion rétablie');
        this.isOnline = true;
        this.updateConnectionStatus();
        this.syncAll();
        this.showNotification('Connexion rétablie', 'Synchronisation en cours...', 'success');
    }

    /**
     * Gestion du passage hors-ligne
     */
    handleOffline() {
        console.log('[Data Sync] Connexion perdue');
        this.isOnline = false;
        this.updateConnectionStatus();
        this.showNotification('Mode hors-ligne', 'Vous pouvez continuer à utiliser l\'application', 'warning');
    }

    /**
     * Met à jour l'indicateur de statut de connexion
     */
    updateConnectionStatus() {
        const statusIndicator = document.getElementById('connection-status');
        if (statusIndicator) {
            if (this.isOnline) {
                statusIndicator.innerHTML = '<i class="fas fa-wifi text-success"></i> En ligne';
                statusIndicator.className = 'badge bg-success';
            } else {
                statusIndicator.innerHTML = '<i class="fas fa-wifi-slash text-warning"></i> Hors-ligne';
                statusIndicator.className = 'badge bg-warning';
            }
        }
    }

    /**
     * Synchronisation complète de toutes les données
     */
    async syncAll() {
        if (this.isSyncing) {
            console.log('[Data Sync] Synchronisation déjà en cours');
            return;
        }

        this.isSyncing = true;
        console.log('[Data Sync] Début de la synchronisation...');

        try {
            await farmConnectDB.init();

            // Synchronisation des cultures
            await this.syncCrops();

            // Synchronisation des types de sol
            await this.syncSoilTypes();

            // Synchronisation des recommandations
            await this.syncRecommendations();

            // Synchronisation des données météo
            await this.syncWeather();

            // Envoi des données en attente
            await this.uploadPendingData();

            // Nettoyage des anciennes données
            await farmConnectDB.cleanOldWeather();

            this.lastSyncTime = new Date();
            console.log('[Data Sync] Synchronisation terminée avec succès');

            // Mise à jour de l'affichage
            this.updateLastSyncDisplay();

        } catch (error) {
            console.error('[Data Sync] Erreur lors de la synchronisation:', error);
        } finally {
            this.isSyncing = false;
        }
    }

    /**
     * Synchronise les cultures depuis le serveur
     */
    async syncCrops() {
        try {
            const response = await fetch('/api/crops/');
            if (!response.ok) throw new Error('Erreur de récupération des cultures');

            const crops = await response.json();
            await farmConnectDB.saveCrops(crops);

            console.log(`[Data Sync] ${crops.length} cultures synchronisées`);
        } catch (error) {
            console.error('[Data Sync] Erreur synchronisation cultures:', error);
        }
    }

    /**
     * Synchronise les types de sol depuis le serveur
     */
    async syncSoilTypes() {
        try {
            const response = await fetch('/api/soil-types/');
            if (!response.ok) throw new Error('Erreur de récupération des types de sol');

            const soilTypes = await response.json();
            await farmConnectDB.saveSoilTypes(soilTypes);

            console.log(`[Data Sync] ${soilTypes.length} types de sol synchronisés`);
        } catch (error) {
            console.error('[Data Sync] Erreur synchronisation types de sol:', error);
        }
    }

    /**
     * Synchronise les recommandations depuis le serveur
     */
    async syncRecommendations() {
        try {
            const response = await fetch('/api/recommendations/');
            if (!response.ok) throw new Error('Erreur de récupération des recommandations');

            const recommendations = await response.json();
            await farmConnectDB.saveRecommendations(recommendations);

            console.log(`[Data Sync] ${recommendations.length} recommandations synchronisées`);
        } catch (error) {
            console.error('[Data Sync] Erreur synchronisation recommandations:', error);
        }
    }

    /**
     * Synchronise les données météo pour la région de l'utilisateur
     */
    async syncWeather() {
        try {
            // Récupérer la région depuis le profil utilisateur ou localStorage
            const userRegion = localStorage.getItem('userRegion') || 'Dakar';

            const response = await fetch(`/api/weather/?region=${userRegion}`);
            if (!response.ok) throw new Error('Erreur de récupération de la météo');

            const weather = await response.json();
            await farmConnectDB.saveWeather({
                region: userRegion,
                data: weather
            });

            console.log(`[Data Sync] Météo synchronisée pour ${userRegion}`);
        } catch (error) {
            console.error('[Data Sync] Erreur synchronisation météo:', error);
        }
    }

    /**
     * Envoie les données en attente de synchronisation au serveur
     */
    async uploadPendingData() {
        try {
            const pendingData = await farmConnectDB.getPendingSync();

            if (pendingData.length === 0) {
                console.log('[Data Sync] Aucune donnée en attente');
                return;
            }

            console.log(`[Data Sync] ${pendingData.length} éléments à synchroniser`);

            for (const item of pendingData) {
                try {
                    const response = await fetch('/api/sync/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this.getCookie('csrftoken')
                        },
                        body: JSON.stringify(item)
                    });

                    if (response.ok) {
                        await farmConnectDB.markAsSynced(item.id);
                        console.log(`[Data Sync] Élément ${item.id} synchronisé`);
                    }
                } catch (error) {
                    console.error(`[Data Sync] Erreur synchronisation élément ${item.id}:`, error);
                }
            }
        } catch (error) {
            console.error('[Data Sync] Erreur upload données en attente:', error);
        }
    }

    /**
     * Récupère les recommandations pour une culture et un type de sol
     * Essaie d'abord en ligne, puis utilise le cache local
     */
    async getRecommendations(cropId, soilTypeId) {
        if (this.isOnline) {
            try {
                const response = await fetch(`/api/recommendations/?crop=${cropId}&soil=${soilTypeId}`);
                if (response.ok) {
                    return await response.json();
                }
            } catch (error) {
                console.log('[Data Sync] Erreur réseau, utilisation du cache');
            }
        }

        // Fallback sur la base locale
        return await farmConnectDB.getRecommendations(cropId, soilTypeId);
    }

    /**
     * Récupère une culture par son ID
     * Essaie d'abord en ligne, puis utilise le cache local
     */
    async getCrop(cropId) {
        if (this.isOnline) {
            try {
                const response = await fetch(`/api/crops/${cropId}/`);
                if (response.ok) {
                    return await response.json();
                }
            } catch (error) {
                console.log('[Data Sync] Erreur réseau, utilisation du cache');
            }
        }

        // Fallback sur la base locale
        return await farmConnectDB.getCropById(cropId);
    }

    /**
     * Récupère toutes les cultures
     * Essaie d'abord en ligne, puis utilise le cache local
     */
    async getAllCrops() {
        if (this.isOnline) {
            try {
                const response = await fetch('/api/crops/');
                if (response.ok) {
                    const crops = await response.json();
                    // Mise à jour du cache local
                    await farmConnectDB.saveCrops(crops);
                    return crops;
                }
            } catch (error) {
                console.log('[Data Sync] Erreur réseau, utilisation du cache');
            }
        }

        // Fallback sur la base locale
        return await farmConnectDB.getAllCrops();
    }

    /**
     * Obtient le cookie CSRF pour les requêtes POST
     */
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Affiche une notification à l'utilisateur
     */
    showNotification(title, message, type = 'info') {
        // Vérifier si l'élément de notification existe
        let notifContainer = document.getElementById('notification-container');
        if (!notifContainer) {
            notifContainer = document.createElement('div');
            notifContainer.id = 'notification-container';
            notifContainer.style.position = 'fixed';
            notifContainer.style.top = '80px';
            notifContainer.style.right = '20px';
            notifContainer.style.zIndex = '9999';
            document.body.appendChild(notifContainer);
        }

        const alertClass = {
            'success': 'alert-success',
            'warning': 'alert-warning',
            'error': 'alert-danger',
            'info': 'alert-info'
        }[type] || 'alert-info';

        const notification = document.createElement('div');
        notification.className = `alert ${alertClass} alert-dismissible fade show`;
        notification.style.minWidth = '300px';
        notification.innerHTML = `
            <strong>${title}</strong><br>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        notifContainer.appendChild(notification);

        // Auto-suppression après 5 secondes
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    /**
     * Met à jour l'affichage de la dernière synchronisation
     */
    updateLastSyncDisplay() {
        const lastSyncElement = document.getElementById('last-sync-time');
        if (lastSyncElement && this.lastSyncTime) {
            const timeAgo = this.getTimeAgo(this.lastSyncTime);
            lastSyncElement.textContent = `Dernière synchro: ${timeAgo}`;
        }
    }

    /**
     * Calcule le temps écoulé depuis une date
     */
    getTimeAgo(date) {
        const seconds = Math.floor((new Date() - date) / 1000);

        if (seconds < 60) return 'À l\'instant';
        if (seconds < 3600) return `Il y a ${Math.floor(seconds / 60)} min`;
        if (seconds < 86400) return `Il y a ${Math.floor(seconds / 3600)}h`;
        return `Il y a ${Math.floor(seconds / 86400)}j`;
    }

    /**
     * Obtient les statistiques de la base de données locale
     */
    async getDatabaseStats() {
        return await farmConnectDB.getDatabaseSize();
    }

    /**
     * Force une synchronisation manuelle
     */
    async forceSync() {
        if (!this.isOnline) {
            this.showNotification('Erreur', 'Vous êtes hors-ligne', 'error');
            return;
        }

        this.showNotification('Synchronisation', 'Synchronisation en cours...', 'info');
        await this.syncAll();
        this.showNotification('Succès', 'Synchronisation terminée', 'success');
    }
}

// Instance globale
const dataSync = new DataSync();

// Export pour utilisation dans d'autres scripts
if (typeof window !== 'undefined') {
    window.dataSync = dataSync;
}

console.log('[Data Sync] Script chargé');
