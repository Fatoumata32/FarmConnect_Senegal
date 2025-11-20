/**
 * Initialisation de la PWA (Progressive Web App) pour FarmConnect
 * Gère l'enregistrement du Service Worker et l'installation de l'application
 */

class PWAManager {
    constructor() {
        this.deferredPrompt = null;
        this.isInstalled = false;
        this.serviceWorkerRegistration = null;

        this.init();
    }

    /**
     * Initialisation
     */
    async init() {
        // Vérifier si le navigateur supporte les Service Workers
        if ('serviceWorker' in navigator) {
            await this.registerServiceWorker();
        } else {
            console.warn('[PWA] Service Workers non supportés');
        }

        // Gérer l'événement beforeinstallprompt
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallButton();
        });

        // Détecter si l'app est déjà installée
        window.addEventListener('appinstalled', () => {
            console.log('[PWA] Application installée');
            this.isInstalled = true;
            this.hideInstallButton();
        });

        // Vérifier si l'app est lancée en mode standalone
        if (window.matchMedia('(display-mode: standalone)').matches) {
            console.log('[PWA] Application en mode standalone');
            this.isInstalled = true;
        }

        console.log('[PWA] Initialisation terminée');
    }

    /**
     * Enregistre le Service Worker
     */
    async registerServiceWorker() {
        try {
            this.serviceWorkerRegistration = await navigator.serviceWorker.register('/static/js/service-worker.js', {
                scope: '/'
            });

            console.log('[PWA] Service Worker enregistré:', this.serviceWorkerRegistration.scope);

            // Écouter les mises à jour du Service Worker
            this.serviceWorkerRegistration.addEventListener('updatefound', () => {
                const newWorker = this.serviceWorkerRegistration.installing;
                console.log('[PWA] Nouvelle version du Service Worker détectée');

                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // Une nouvelle version est disponible
                        this.showUpdateNotification();
                    }
                });
            });

            // Vérifier périodiquement les mises à jour
            setInterval(() => {
                this.serviceWorkerRegistration.update();
            }, 60 * 60 * 1000); // Toutes les heures

        } catch (error) {
            console.error('[PWA] Erreur d\'enregistrement du Service Worker:', error);
        }
    }

    /**
     * Affiche le bouton d'installation
     */
    showInstallButton() {
        const installButton = document.getElementById('install-app-button');
        if (installButton) {
            installButton.style.display = 'block';
            installButton.addEventListener('click', () => this.installApp());
        }

        // Afficher une bannière d'installation
        this.showInstallBanner();
    }

    /**
     * Cache le bouton d'installation
     */
    hideInstallButton() {
        const installButton = document.getElementById('install-app-button');
        if (installButton) {
            installButton.style.display = 'none';
        }

        this.hideInstallBanner();
    }

    /**
     * Affiche une bannière d'installation
     */
    showInstallBanner() {
        // Ne pas afficher si déjà installé
        if (this.isInstalled) return;

        // Ne pas afficher si déjà fermée récemment
        const bannerDismissed = localStorage.getItem('install-banner-dismissed');
        if (bannerDismissed) {
            const dismissedTime = new Date(bannerDismissed);
            const now = new Date();
            const daysSinceDismissed = (now - dismissedTime) / (1000 * 60 * 60 * 24);

            if (daysSinceDismissed < 7) {
                return; // Ne pas réafficher avant 7 jours
            }
        }

        // Créer la bannière
        const banner = document.createElement('div');
        banner.id = 'install-banner';
        banner.className = 'alert alert-success alert-dismissible fade show';
        banner.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            max-width: 500px;
            z-index: 9999;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        `;

        banner.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-download fa-2x me-3 text-success"></i>
                <div class="flex-grow-1">
                    <strong>Installer FarmConnect</strong><br>
                    <small>Accédez plus rapidement et utilisez l'app hors-ligne</small>
                </div>
                <button type="button" class="btn btn-success btn-sm ms-3" id="install-banner-button">
                    <i class="fas fa-plus"></i> Installer
                </button>
                <button type="button" class="btn-close ms-2" id="install-banner-close"></button>
            </div>
        `;

        document.body.appendChild(banner);

        // Bouton d'installation
        document.getElementById('install-banner-button').addEventListener('click', () => {
            this.installApp();
            banner.remove();
        });

        // Bouton de fermeture
        document.getElementById('install-banner-close').addEventListener('click', () => {
            localStorage.setItem('install-banner-dismissed', new Date().toISOString());
            banner.remove();
        });
    }

    /**
     * Cache la bannière d'installation
     */
    hideInstallBanner() {
        const banner = document.getElementById('install-banner');
        if (banner) {
            banner.remove();
        }
    }

    /**
     * Lance l'installation de l'application
     */
    async installApp() {
        if (!this.deferredPrompt) {
            console.warn('[PWA] Aucune invitation d\'installation disponible');
            return;
        }

        // Afficher la boîte de dialogue d'installation
        this.deferredPrompt.prompt();

        // Attendre la réponse de l'utilisateur
        const { outcome } = await this.deferredPrompt.userChoice;
        console.log(`[PWA] Installation: ${outcome}`);

        if (outcome === 'accepted') {
            this.isInstalled = true;
            this.hideInstallButton();
        }

        // Réinitialiser le prompt
        this.deferredPrompt = null;
    }

    /**
     * Affiche une notification de mise à jour disponible
     */
    showUpdateNotification() {
        const updateNotif = document.createElement('div');
        updateNotif.className = 'alert alert-info alert-dismissible fade show';
        updateNotif.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            max-width: 400px;
            z-index: 9999;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        `;

        updateNotif.innerHTML = `
            <strong><i class="fas fa-sync-alt"></i> Mise à jour disponible</strong><br>
            <small>Une nouvelle version de FarmConnect est disponible</small><br>
            <button type="button" class="btn btn-primary btn-sm mt-2" id="update-app-button">
                <i class="fas fa-download"></i> Mettre à jour
            </button>
            <button type="button" class="btn-close ms-2"></button>
        `;

        document.body.appendChild(updateNotif);

        document.getElementById('update-app-button').addEventListener('click', () => {
            this.updateApp();
            updateNotif.remove();
        });

        updateNotif.querySelector('.btn-close').addEventListener('click', () => {
            updateNotif.remove();
        });
    }

    /**
     * Met à jour l'application
     */
    updateApp() {
        if (this.serviceWorkerRegistration && this.serviceWorkerRegistration.waiting) {
            // Envoyer un message au Service Worker pour qu'il prenne le contrôle
            this.serviceWorkerRegistration.waiting.postMessage({ type: 'SKIP_WAITING' });

            // Recharger la page une fois le nouveau SW activé
            navigator.serviceWorker.addEventListener('controllerchange', () => {
                window.location.reload();
            });
        }
    }

    /**
     * Vérifie si l'application est en mode hors-ligne
     */
    isOffline() {
        return !navigator.onLine;
    }

    /**
     * Obtient des informations sur le Service Worker
     */
    getServiceWorkerInfo() {
        if (!this.serviceWorkerRegistration) {
            return null;
        }

        return {
            scope: this.serviceWorkerRegistration.scope,
            active: !!this.serviceWorkerRegistration.active,
            installing: !!this.serviceWorkerRegistration.installing,
            waiting: !!this.serviceWorkerRegistration.waiting
        };
    }

    /**
     * Désinstalle le Service Worker (pour debug uniquement)
     */
    async unregisterServiceWorker() {
        if (this.serviceWorkerRegistration) {
            const success = await this.serviceWorkerRegistration.unregister();
            console.log('[PWA] Service Worker désinstallé:', success);
            return success;
        }
        return false;
    }
}

// Instance globale
const pwaManager = new PWAManager();

// Export pour utilisation dans d'autres scripts
if (typeof window !== 'undefined') {
    window.pwaManager = pwaManager;
}

console.log('[PWA] Script d\'initialisation chargé');
