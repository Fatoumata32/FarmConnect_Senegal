/**
 * Gestion des modals pour afficher les détails des cultures
 * Charge dynamiquement les données depuis l'API
 */

class CropModalManager {
    constructor() {
        this.currentCrop = null;
        this.language = 'fr'; // ou 'wo' pour wolof
        this.init();
    }

    init() {
        // Créer le modal principal une seule fois
        this.createModalTemplate();

        // Écouter les clics sur les cartes de cultures
        document.addEventListener('click', (e) => {
            const cropCard = e.target.closest('[data-crop-id]');
            if (cropCard) {
                const cropId = cropCard.dataset.cropId;
                this.openCropModal(cropId);
            }
        });

        console.log('[Crop Modals] Gestionnaire initialisé');
    }

    /**
     * Crée le template HTML du modal
     */
    createModalTemplate() {
        const modalHTML = `
            <div class="modal fade" id="cropDetailModal" tabindex="-1" aria-labelledby="cropDetailModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-xl modal-dialog-scrollable">
                    <div class="modal-content">
                        <div class="modal-header" style="background: linear-gradient(135deg, #2d5016 0%, #4a7c59 100%); color: white;">
                            <h5 class="modal-title" id="cropDetailModalLabel">
                                <i class="fas fa-leaf"></i> <span id="cropName">Chargement...</span>
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" id="cropModalBody">
                            <div class="text-center py-5">
                                <div class="spinner-border text-success" role="status">
                                    <span class="visually-hidden">Chargement...</span>
                                </div>
                                <p class="mt-3">Chargement des informations...</p>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-times"></i> Fermer
                            </button>
                            <button type="button" class="btn btn-success" id="addToFavorites">
                                <i class="fas fa-star"></i> Ajouter aux favoris
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Ajouter le modal au body s'il n'existe pas
        if (!document.getElementById('cropDetailModal')) {
            document.body.insertAdjacentHTML('beforeend', modalHTML);
        }
    }

    /**
     * Ouvre le modal et charge les données de la culture
     */
    async openCropModal(cropId) {
        const modal = new bootstrap.Modal(document.getElementById('cropDetailModal'));
        modal.show();

        // Réinitialiser le contenu
        document.getElementById('cropName').textContent = 'Chargement...';
        document.getElementById('cropModalBody').innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">Chargement...</span>
                </div>
                <p class="mt-3">Chargement des informations...</p>
            </div>
        `;

        try {
            // Charger les données (d'abord en ligne, puis cache si hors-ligne)
            const cropData = await this.loadCropData(cropId);
            this.currentCrop = cropData;

            // Afficher les données
            this.renderCropDetails(cropData);

        } catch (error) {
            console.error('[Crop Modal] Erreur de chargement:', error);
            this.showError();
        }
    }

    /**
     * Charge les données d'une culture
     */
    async loadCropData(cropId) {
        // Essayer de charger depuis le serveur
        if (navigator.onLine) {
            try {
                const response = await fetch(`/crops/api/${cropId}/?lang=${this.language}`);
                if (!response.ok) throw new Error('Erreur serveur');

                const data = await response.json();

                // Sauvegarder dans IndexedDB pour utilisation hors-ligne
                if (window.farmConnectDB) {
                    await window.farmConnectDB.saveCrops([data]);
                }

                return data;
            } catch (error) {
                console.log('[Crop Modal] Erreur réseau, tentative cache local');
            }
        }

        // Fallback sur IndexedDB si hors-ligne ou erreur
        if (window.farmConnectDB) {
            const cachedCrop = await window.farmConnectDB.getCropById(cropId);
            if (cachedCrop) {
                return cachedCrop;
            }
        }

        throw new Error('Impossible de charger les données');
    }

    /**
     * Affiche les détails de la culture dans le modal
     */
    renderCropDetails(crop) {
        document.getElementById('cropName').innerHTML = `
            ${crop.name}
            ${crop.scientific_name ? `<small class="text-white-50">(${crop.scientific_name})</small>` : ''}
        `;

        const content = `
            <div class="container-fluid">
                <div class="row">
                    <!-- Colonne gauche: Image et infos de base -->
                    <div class="col-md-4">
                        ${crop.image ? `
                            <img src="${crop.image}" class="img-fluid rounded shadow mb-3" alt="${crop.name}">
                        ` : `
                            <div class="bg-light rounded p-5 text-center mb-3">
                                <i class="fas fa-seedling fa-5x text-success"></i>
                            </div>
                        `}

                        <div class="card shadow-sm mb-3">
                            <div class="card-body">
                                <h6 class="card-title text-success">
                                    <i class="fas fa-info-circle"></i> Informations générales
                                </h6>
                                <ul class="list-unstyled mb-0">
                                    <li class="mb-2">
                                        <strong><i class="fas fa-tag"></i> Catégorie:</strong><br>
                                        <span class="badge bg-success">${crop.category}</span>
                                    </li>
                                    <li class="mb-2">
                                        <strong><i class="fas fa-calendar"></i> Saison:</strong><br>
                                        ${crop.growing_season}
                                    </li>
                                    <li class="mb-2">
                                        <strong><i class="fas fa-clock"></i> Durée du cycle:</strong><br>
                                        ${crop.growth_duration_days ? crop.growth_duration_days + ' jours' : 'N/A'}
                                    </li>
                                    <li class="mb-2">
                                        <strong><i class="fas fa-chart-line"></i> Rendement moyen:</strong><br>
                                        ${crop.average_yield || 'N/A'}
                                    </li>
                                </ul>
                            </div>
                        </div>

                        ${crop.drought_resistant || crop.flood_tolerant ? `
                            <div class="card shadow-sm mb-3">
                                <div class="card-body">
                                    <h6 class="card-title text-success">
                                        <i class="fas fa-shield-alt"></i> Résistances
                                    </h6>
                                    ${crop.drought_resistant ? '<span class="badge bg-warning text-dark me-2"><i class="fas fa-sun"></i> Résistant à la sécheresse</span>' : ''}
                                    ${crop.flood_tolerant ? '<span class="badge bg-info"><i class="fas fa-water"></i> Tolérant aux inondations</span>' : ''}
                                </div>
                            </div>
                        ` : ''}
                    </div>

                    <!-- Colonne droite: Détails techniques -->
                    <div class="col-md-8">
                        ${crop.description ? `
                            <div class="alert alert-light shadow-sm mb-3">
                                <i class="fas fa-align-left text-success"></i> ${crop.description}
                            </div>
                        ` : ''}

                        <!-- Onglets -->
                        <ul class="nav nav-pills mb-3" id="cropTabs" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active" id="calendar-tab" data-bs-toggle="pill" data-bs-target="#calendar" type="button">
                                    <i class="fas fa-calendar-alt"></i> Calendrier
                                </button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="climate-tab" data-bs-toggle="pill" data-bs-target="#climate" type="button">
                                    <i class="fas fa-cloud-sun"></i> Climat
                                </button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="soil-tab" data-bs-toggle="pill" data-bs-target="#soil" type="button">
                                    <i class="fas fa-layer-group"></i> Sol
                                </button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="techniques-tab" data-bs-toggle="pill" data-bs-target="#techniques" type="button">
                                    <i class="fas fa-tools"></i> Techniques
                                </button>
                            </li>
                            ${crop.recommendations && crop.recommendations.length > 0 ? `
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="recommendations-tab" data-bs-toggle="pill" data-bs-target="#recommendations" type="button">
                                        <i class="fas fa-lightbulb"></i> Recommandations
                                    </button>
                                </li>
                            ` : ''}
                        </ul>

                        <div class="tab-content" id="cropTabsContent">
                            <!-- Onglet Calendrier -->
                            <div class="tab-pane fade show active" id="calendar" role="tabpanel">
                                <div class="card shadow-sm">
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-md-4 mb-3">
                                                <div class="text-center p-3 bg-light rounded">
                                                    <i class="fas fa-seedling fa-2x text-success mb-2"></i>
                                                    <h6>Plantation</h6>
                                                    <p class="mb-0">${crop.planting_period}</p>
                                                </div>
                                            </div>
                                            <div class="col-md-4 mb-3">
                                                <div class="text-center p-3 bg-light rounded">
                                                    <i class="fas fa-clock fa-2x text-warning mb-2"></i>
                                                    <h6>Durée</h6>
                                                    <p class="mb-0">${crop.growth_duration_days ? crop.growth_duration_days + ' jours' : 'N/A'}</p>
                                                </div>
                                            </div>
                                            <div class="col-md-4 mb-3">
                                                <div class="text-center p-3 bg-light rounded">
                                                    <i class="fas fa-apple-alt fa-2x text-danger mb-2"></i>
                                                    <h6>Récolte</h6>
                                                    <p class="mb-0">${crop.harvest_period}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Onglet Climat -->
                            <div class="tab-pane fade" id="climate" role="tabpanel">
                                <div class="card shadow-sm">
                                    <div class="card-body">
                                        <h6 class="text-success mb-3"><i class="fas fa-thermometer-half"></i> Température</h6>
                                        <div class="row mb-3">
                                            <div class="col-md-4">
                                                <small class="text-muted">Minimale</small><br>
                                                <strong>${crop.min_temperature ? crop.min_temperature + '°C' : 'N/A'}</strong>
                                            </div>
                                            <div class="col-md-4">
                                                <small class="text-muted">Optimale</small><br>
                                                <strong class="text-success">${crop.optimal_temperature ? crop.optimal_temperature + '°C' : 'N/A'}</strong>
                                            </div>
                                            <div class="col-md-4">
                                                <small class="text-muted">Maximale</small><br>
                                                <strong>${crop.max_temperature ? crop.max_temperature + '°C' : 'N/A'}</strong>
                                            </div>
                                        </div>

                                        <h6 class="text-success mb-3"><i class="fas fa-cloud-rain"></i> Pluviométrie</h6>
                                        <div class="row mb-3">
                                            <div class="col-md-6">
                                                <small class="text-muted">Minimum</small><br>
                                                <strong>${crop.min_rainfall ? crop.min_rainfall + ' mm/an' : 'N/A'}</strong>
                                            </div>
                                            <div class="col-md-6">
                                                <small class="text-muted">Maximum</small><br>
                                                <strong>${crop.max_rainfall ? crop.max_rainfall + ' mm/an' : 'N/A'}</strong>
                                            </div>
                                        </div>

                                        <h6 class="text-success mb-3"><i class="fas fa-tint"></i> Besoin en eau</h6>
                                        <div class="progress" style="height: 25px;">
                                            <div class="progress-bar ${this.getWaterRequirementClass(crop.water_requirement)}"
                                                 style="width: ${this.getWaterRequirementWidth(crop.water_requirement)}%">
                                                ${crop.water_requirement}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Onglet Sol -->
                            <div class="tab-pane fade" id="soil" role="tabpanel">
                                <div class="card shadow-sm">
                                    <div class="card-body">
                                        <h6 class="text-success mb-3"><i class="fas fa-layer-group"></i> Types de sol appropriés</h6>
                                        ${crop.soil_types && crop.soil_types.length > 0 ? `
                                            <div class="row">
                                                ${crop.soil_types.map(soil => `
                                                    <div class="col-md-6 mb-3">
                                                        <div class="card h-100">
                                                            <div class="card-body">
                                                                <h6 class="card-title">${soil.name}</h6>
                                                                <p class="card-text small">${soil.description}</p>
                                                                <div class="d-flex flex-wrap gap-1">
                                                                    <span class="badge bg-secondary">${soil.texture}</span>
                                                                    <span class="badge bg-info">${soil.drainage}</span>
                                                                    <span class="badge bg-success">${soil.fertility}</span>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                `).join('')}
                                            </div>
                                        ` : '<p class="text-muted">Aucun type de sol spécifique requis</p>'}

                                        ${crop.min_altitude || crop.max_altitude ? `
                                            <h6 class="text-success mb-3 mt-3"><i class="fas fa-mountain"></i> Altitude</h6>
                                            <p>${crop.min_altitude || 0} - ${crop.max_altitude || 'N/A'} m</p>
                                        ` : ''}
                                    </div>
                                </div>
                            </div>

                            <!-- Onglet Techniques -->
                            <div class="tab-pane fade" id="techniques" role="tabpanel">
                                <div class="card shadow-sm">
                                    <div class="card-body">
                                        <h6 class="text-success mb-3"><i class="fas fa-ruler"></i> Espacement</h6>
                                        <div class="row mb-3">
                                            <div class="col-md-6">
                                                <div class="p-3 bg-light rounded">
                                                    <i class="fas fa-arrows-alt-h text-success"></i>
                                                    <strong> Entre lignes:</strong> ${crop.row_spacing_cm ? crop.row_spacing_cm + ' cm' : 'N/A'}
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="p-3 bg-light rounded">
                                                    <i class="fas fa-arrows-alt text-success"></i>
                                                    <strong> Entre plants:</strong> ${crop.plant_spacing_cm ? crop.plant_spacing_cm + ' cm' : 'N/A'}
                                                </div>
                                            </div>
                                        </div>

                                        ${crop.tips && crop.tips.length > 0 ? `
                                            <h6 class="text-success mb-3"><i class="fas fa-lightbulb"></i> Conseils pratiques</h6>
                                            ${crop.tips.map(tip => `
                                                <div class="alert alert-${tip.urgent ? 'warning' : 'info'} shadow-sm">
                                                    <strong><i class="fas fa-${tip.urgent ? 'exclamation-triangle' : 'info-circle'}"></i> ${tip.title}</strong>
                                                    <p class="mb-0 mt-2">${tip.content}</p>
                                                    <small class="text-muted"><i class="fas fa-tag"></i> ${tip.type}</small>
                                                </div>
                                            `).join('')}
                                        ` : ''}
                                    </div>
                                </div>
                            </div>

                            <!-- Onglet Recommandations -->
                            ${crop.recommendations && crop.recommendations.length > 0 ? `
                                <div class="tab-pane fade" id="recommendations" role="tabpanel">
                                    <div class="card shadow-sm">
                                        <div class="card-body">
                                            ${crop.recommendations.map(reco => `
                                                <div class="mb-4">
                                                    <h6 class="text-success">
                                                        <i class="fas fa-layer-group"></i> ${reco.soil_type} - ${reco.season}
                                                    </h6>
                                                    <div class="accordion" id="reco${crop.id}">
                                                        <div class="accordion-item">
                                                            <h2 class="accordion-header">
                                                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#prep${crop.id}">
                                                                    <i class="fas fa-tractor me-2"></i> Préparation du sol
                                                                </button>
                                                            </h2>
                                                            <div id="prep${crop.id}" class="accordion-collapse collapse">
                                                                <div class="accordion-body">${reco.soil_preparation}</div>
                                                            </div>
                                                        </div>
                                                        <div class="accordion-item">
                                                            <h2 class="accordion-header">
                                                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#fert${crop.id}">
                                                                    <i class="fas fa-flask me-2"></i> Fertilisation
                                                                </button>
                                                            </h2>
                                                            <div id="fert${crop.id}" class="accordion-collapse collapse">
                                                                <div class="accordion-body">${reco.fertilization}</div>
                                                            </div>
                                                        </div>
                                                        <div class="accordion-item">
                                                            <h2 class="accordion-header">
                                                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#irrig${crop.id}">
                                                                    <i class="fas fa-tint me-2"></i> Irrigation
                                                                </button>
                                                            </h2>
                                                            <div id="irrig${crop.id}" class="accordion-collapse collapse">
                                                                <div class="accordion-body">${reco.irrigation}</div>
                                                            </div>
                                                        </div>
                                                        <div class="accordion-item">
                                                            <h2 class="accordion-header">
                                                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#pest${crop.id}">
                                                                    <i class="fas fa-bug me-2"></i> Protection phytosanitaire
                                                                </button>
                                                            </h2>
                                                            <div id="pest${crop.id}" class="accordion-collapse collapse">
                                                                <div class="accordion-body">${reco.pest_management}</div>
                                                            </div>
                                                        </div>
                                                        <div class="accordion-item">
                                                            <h2 class="accordion-header">
                                                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#harv${crop.id}">
                                                                    <i class="fas fa-apple-alt me-2"></i> Récolte
                                                                </button>
                                                            </h2>
                                                            <div id="harv${crop.id}" class="accordion-collapse collapse">
                                                                <div class="accordion-body">
                                                                    ${reco.harvest_advice}
                                                                    ${reco.expected_yield ? `<div class="mt-2"><strong>Rendement attendu:</strong> ${reco.expected_yield}</div>` : ''}
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            `).join('')}
                                        </div>
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('cropModalBody').innerHTML = content;

        // Gérer le bouton favoris
        document.getElementById('addToFavorites').onclick = () => this.addToFavorites(crop.id);
    }

    /**
     * Affiche un message d'erreur
     */
    showError() {
        document.getElementById('cropModalBody').innerHTML = `
            <div class="alert alert-danger text-center">
                <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                <h5>Erreur de chargement</h5>
                <p>Impossible de charger les informations de cette culture.</p>
                <small>Vérifiez votre connexion internet ou réessayez plus tard.</small>
            </div>
        `;
    }

    /**
     * Ajoute une culture aux favoris
     */
    async addToFavorites(cropId) {
        if (window.farmConnectDB) {
            try {
                const userId = 1; // TODO: Récupérer l'ID utilisateur réel
                await window.farmConnectDB.addToFavorites(cropId, userId);

                alert('✅ Culture ajoutée aux favoris !');
            } catch (error) {
                console.error('[Crop Modal] Erreur ajout favoris:', error);
                alert('❌ Erreur lors de l\'ajout aux favoris');
            }
        }
    }

    /**
     * Helpers pour l'affichage
     */
    getWaterRequirementClass(requirement) {
        const classes = {
            'Très élevé': 'bg-danger',
            'Élevé': 'bg-warning',
            'Moyen': 'bg-info',
            'Faible': 'bg-success'
        };
        return classes[requirement] || 'bg-secondary';
    }

    getWaterRequirementWidth(requirement) {
        const widths = {
            'Très élevé': 100,
            'Élevé': 75,
            'Moyen': 50,
            'Faible': 25
        };
        return widths[requirement] || 0;
    }
}

// Initialiser le gestionnaire au chargement de la page
if (typeof window !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        window.cropModalManager = new CropModalManager();
        console.log('[Crop Modals] Gestionnaire prêt');
    });
}
