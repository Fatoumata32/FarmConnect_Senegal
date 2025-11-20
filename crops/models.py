from django.db import models
from farmconnect_app.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class SoilType(models.Model):
    """Types de sol au Sénégal"""
    name_fr = models.CharField(max_length=100, verbose_name="Nom en français")
    name_wo = models.CharField(max_length=100, verbose_name="Nom en wolof")
    description_fr = models.TextField(verbose_name="Description en français")
    description_wo = models.TextField(verbose_name="Description en wolof")

    # Propriétés chimiques
    ph_min = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(14)])
    ph_max = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(14)])

    # Propriétés physiques
    texture = models.CharField(max_length=50, choices=[
        ('argileuse', 'Argileuse'),
        ('sableuse', 'Sableuse'),
        ('limoneuse', 'Limoneuse'),
        ('mixte', 'Mixte'),
    ])
    drainage = models.CharField(max_length=50, choices=[
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('faible', 'Faible'),
    ])
    fertility = models.CharField(max_length=50, choices=[
        ('très_élevée', 'Très élevée'),
        ('élevée', 'Élevée'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible'),
    ])

    # Caractéristiques
    water_retention = models.CharField(max_length=50, choices=[
        ('très_élevée', 'Très élevée'),
        ('élevée', 'Élevée'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible'),
    ], verbose_name="Rétention d'eau")

    organic_matter = models.CharField(max_length=50, choices=[
        ('riche', 'Riche'),
        ('moyen', 'Moyen'),
        ('pauvre', 'Pauvre'),
    ], verbose_name="Matière organique")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Type de sol"
        verbose_name_plural = "Types de sol"
        ordering = ['name_fr']

    def __str__(self):
        return self.name_fr

class Season(models.Model):
    """Saisons agricoles au Sénégal"""
    name_fr = models.CharField(max_length=100, verbose_name="Nom en français")
    name_wo = models.CharField(max_length=100, verbose_name="Nom en wolof")
    start_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    end_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    description_fr = models.TextField(blank=True)
    description_wo = models.TextField(blank=True)

    class Meta:
        verbose_name = "Saison"
        verbose_name_plural = "Saisons"
        ordering = ['start_month']

    def __str__(self):
        return self.name_fr

class Crop(models.Model):
    """Modèle pour les différentes cultures"""
    name_fr = models.CharField(max_length=100, verbose_name="Nom en français")
    name_wo = models.CharField(max_length=100, verbose_name="Nom en wolof")
    scientific_name = models.CharField(max_length=100, blank=True, verbose_name="Nom scientifique")
    category = models.CharField(max_length=50, choices=[
        ('cereales', 'Céréales'),
        ('legumineuses', 'Légumineuses'),
        ('legumes', 'Légumes'),
        ('fruits', 'Fruits'),
        ('tubercules', 'Tubercules'),
        ('cultures_rente', 'Cultures de rente'),
        ('oleagineux', 'Oléagineux'),
        ('epices', 'Épices et aromates'),
    ])
    growing_season = models.CharField(max_length=100, verbose_name="Saison de culture")
    planting_period = models.CharField(max_length=100, verbose_name="Période de plantation")
    harvest_period = models.CharField(max_length=100, verbose_name="Période de récolte")

    # Nouveaux champs pour recommandations personnalisées
    suitable_soil_types = models.ManyToManyField(SoilType, related_name='crops', blank=True, verbose_name="Types de sol appropriés")

    # Besoins en eau
    water_requirement = models.CharField(max_length=50, choices=[
        ('très_élevé', 'Très élevé'),
        ('élevé', 'Élevé'),
        ('moyen', 'Moyen'),
        ('faible', 'Faible'),
    ], default='moyen', verbose_name="Besoin en eau")

    # Altitude
    min_altitude = models.IntegerField(null=True, blank=True, verbose_name="Altitude minimale (m)")
    max_altitude = models.IntegerField(null=True, blank=True, verbose_name="Altitude maximale (m)")

    # Température
    min_temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Température minimale (°C)")
    max_temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Température maximale (°C)")
    optimal_temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Température optimale (°C)")

    # Pluviométrie
    min_rainfall = models.IntegerField(null=True, blank=True, verbose_name="Pluviométrie minimale (mm/an)")
    max_rainfall = models.IntegerField(null=True, blank=True, verbose_name="Pluviométrie maximale (mm/an)")

    # Cycle de culture
    growth_duration_days = models.IntegerField(null=True, blank=True, verbose_name="Durée du cycle (jours)")

    # Résistance
    drought_resistant = models.BooleanField(default=False, verbose_name="Résistant à la sécheresse")
    flood_tolerant = models.BooleanField(default=False, verbose_name="Tolérant aux inondations")

    # Espacement
    row_spacing_cm = models.IntegerField(null=True, blank=True, verbose_name="Espacement entre lignes (cm)")
    plant_spacing_cm = models.IntegerField(null=True, blank=True, verbose_name="Espacement entre plants (cm)")

    # Rendement
    average_yield = models.CharField(max_length=100, blank=True, verbose_name="Rendement moyen")

    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='crops/', null=True, blank=True)
    description_fr = models.TextField(blank=True)
    description_wo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_fr

    class Meta:
        verbose_name = "Culture"
        verbose_name_plural = "Cultures"
        ordering = ['name_fr']

class CropTip(models.Model):
    """Conseils agricoles pour les cultures"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='tips')
    title_fr = models.CharField(max_length=200, verbose_name="Titre en français")
    title_wo = models.CharField(max_length=200, verbose_name="Titre en wolof")
    content_fr = models.TextField(verbose_name="Contenu en français")
    content_wo = models.TextField(verbose_name="Contenu en wolof")
    tip_type = models.CharField(max_length=50, choices=[
        ('planting', 'Plantation'),
        ('care', 'Entretien'),
        ('fertilization', 'Fertilisation'),
        ('irrigation', 'Irrigation'),
        ('pest_control', 'Lutte antiparasitaire'),
        ('harvest', 'Récolte'),
        ('storage', 'Conservation'),
    ])
    season = models.CharField(max_length=50, blank=True)
    is_urgent = models.BooleanField(default=False, verbose_name="Conseil urgent")
    priority = models.IntegerField(default=1, choices=[
        (1, 'Faible'),
        (2, 'Normale'),
        (3, 'Élevée'),
        (4, 'Critique'),
    ])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = "Conseil agricole"
        verbose_name_plural = "Conseils agricoles"

    def __str__(self):
        return f"{self.title_fr} - {self.crop.name_fr}"

class CropSoilRecommendation(models.Model):
    """Recommandations spécifiques par culture, type de sol et saison"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='soil_recommendations')
    soil_type = models.ForeignKey(SoilType, on_delete=models.CASCADE, related_name='crop_recommendations')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='recommendations', null=True, blank=True)

    # Préparation du sol
    soil_preparation_fr = models.TextField(verbose_name="Préparation du sol (FR)")
    soil_preparation_wo = models.TextField(verbose_name="Préparation du sol (WO)", blank=True)

    # Fertilisation
    fertilization_fr = models.TextField(verbose_name="Fertilisation (FR)")
    fertilization_wo = models.TextField(verbose_name="Fertilisation (WO)", blank=True)

    # Irrigation
    irrigation_fr = models.TextField(verbose_name="Irrigation (FR)")
    irrigation_wo = models.TextField(verbose_name="Irrigation (WO)", blank=True)

    # Protection phytosanitaire
    pest_management_fr = models.TextField(verbose_name="Lutte contre maladies/ravageurs (FR)")
    pest_management_wo = models.TextField(verbose_name="Lutte contre maladies/ravageurs (WO)", blank=True)

    # Récolte
    harvest_advice_fr = models.TextField(verbose_name="Conseils de récolte (FR)")
    harvest_advice_wo = models.TextField(verbose_name="Conseils de récolte (WO)", blank=True)

    # Stockage
    storage_advice_fr = models.TextField(verbose_name="Conseils de stockage (FR)", blank=True)
    storage_advice_wo = models.TextField(verbose_name="Conseils de stockage (WO)", blank=True)

    # Amendements recommandés
    recommended_amendments_fr = models.TextField(verbose_name="Amendements recommandés (FR)", blank=True)
    recommended_amendments_wo = models.TextField(verbose_name="Amendements recommandés (WO)", blank=True)

    # Espacement recommandé pour ce type de sol
    recommended_row_spacing = models.IntegerField(null=True, blank=True, verbose_name="Espacement lignes recommandé (cm)")
    recommended_plant_spacing = models.IntegerField(null=True, blank=True, verbose_name="Espacement plants recommandé (cm)")

    # Rendement attendu
    expected_yield = models.CharField(max_length=200, blank=True, verbose_name="Rendement attendu")

    # Conditions optimales
    optimal_conditions_fr = models.TextField(verbose_name="Conditions optimales (FR)", blank=True)
    optimal_conditions_wo = models.TextField(verbose_name="Conditions optimales (WO)", blank=True)

    # Précautions spécifiques
    warnings_fr = models.TextField(verbose_name="Précautions/Avertissements (FR)", blank=True)
    warnings_wo = models.TextField(verbose_name="Précautions/Avertissements (WO)", blank=True)

    # Priorité de la recommandation
    priority = models.IntegerField(default=2, choices=[
        (1, 'Faible'),
        (2, 'Normale'),
        (3, 'Élevée'),
    ])

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recommandation culture-sol"
        verbose_name_plural = "Recommandations culture-sol"
        ordering = ['-priority', 'crop__name_fr']
        unique_together = ['crop', 'soil_type', 'season']

    def __str__(self):
        season_str = f" - {self.season.name_fr}" if self.season else ""
        return f"{self.crop.name_fr} sur {self.soil_type.name_fr}{season_str}"
