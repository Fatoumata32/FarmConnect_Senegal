"""
Models for Advice Library and Decision Tree System
Replaces chatbot with structured, offline-friendly advice
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class AdviceEntry(models.Model):
    """
    Individual advice entry - searchable, filterable, offline-cacheable
    """
    LANGUAGE_CHOICES = (
        ('fr', 'Français'),
        ('wo', 'Wolof'),
        ('en', 'English'),
    )

    STAGE_CHOICES = (
        ('planting', 'Plantation'),
        ('growth', 'Croissance'),
        ('flowering', 'Floraison'),
        ('fruiting', 'Fructification'),
        ('harvest', 'Récolte'),
        ('post_harvest', 'Post-récolte'),
        ('general', 'Général'),
    )

    SEVERITY_CHOICES = (
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Élevé'),
        ('critical', 'Critique'),
    )

    CATEGORY_CHOICES = (
        ('pest', 'Ravageurs'),
        ('disease', 'Maladies'),
        ('nutrient', 'Nutrition'),
        ('watering', 'Irrigation'),
        ('soil', 'Sol'),
        ('weather', 'Météo'),
        ('harvest', 'Récolte'),
        ('storage', 'Stockage'),
        ('general', 'Général'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Titles in multiple languages
    title_fr = models.CharField(max_length=255, verbose_name="Titre (Français)")
    title_wo = models.CharField(max_length=255, blank=True, verbose_name="Titre (Wolof)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Title (English)")

    crop = models.ForeignKey(
        'crops.Crop',
        on_delete=models.CASCADE,
        related_name='advice_entries',
        verbose_name="Culture"
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Catégorie"
    )

    # Tags as simple comma-separated text (works without postgres ArrayField)
    tags = models.TextField(
        blank=True,
        verbose_name="Tags",
        help_text="Tags séparés par des virgules (ex: soil:sandy, season:dry)"
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='fr',
        verbose_name="Langue principale"
    )

    stage = models.CharField(
        max_length=50,
        choices=STAGE_CHOICES,
        verbose_name="Stade de croissance"
    )

    # Content in multiple languages
    content_fr = models.TextField(verbose_name="Contenu (Français)")
    content_wo = models.TextField(blank=True, verbose_name="Contenu (Wolof)")
    content_en = models.TextField(blank=True, verbose_name="Content (English)")

    short_description_fr = models.TextField(
        max_length=500,
        verbose_name="Description courte (Français)"
    )
    short_description_wo = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Description courte (Wolof)"
    )
    short_description_en = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Short description (English)"
    )

    # Action steps as text (will be parsed as list in frontend)
    action_steps_fr = models.TextField(
        blank=True,
        verbose_name="Étapes d'action (Français)",
        help_text="Une étape par ligne"
    )
    action_steps_wo = models.TextField(
        blank=True,
        verbose_name="Étapes d'action (Wolof)",
        help_text="Une étape par ligne"
    )
    action_steps_en = models.TextField(
        blank=True,
        verbose_name="Action steps (English)",
        help_text="One step per line"
    )

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='low',
        verbose_name="Sévérité"
    )

    # Metadata
    view_count = models.IntegerField(default=0, verbose_name="Nombre de vues")
    helpful_count = models.IntegerField(default=0, verbose_name="Utile")
    not_helpful_count = models.IntegerField(default=0, verbose_name="Pas utile")

    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_featured = models.BooleanField(default=False, verbose_name="En vedette")
    priority = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Priorité",
        help_text="Plus élevé = plus visible"
    )

    # Authoring
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='advice_entries',
        verbose_name="Auteur"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    version = models.IntegerField(default=1, verbose_name="Version")

    class Meta:
        verbose_name = "Conseil agricole"
        verbose_name_plural = "Conseils agricoles"
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['crop', 'category', 'stage']),
            models.Index(fields=['is_active', '-priority']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.title_fr} ({self.crop.name_fr if self.crop else 'No crop'})"

    def get_title(self, language='fr'):
        """Get title in specified language with fallback"""
        if language == 'wo' and self.title_wo:
            return self.title_wo
        elif language == 'en' and self.title_en:
            return self.title_en
        return self.title_fr

    def get_content(self, language='fr'):
        """Get content in specified language with fallback"""
        if language == 'wo' and self.content_wo:
            return self.content_wo
        elif language == 'en' and self.content_en:
            return self.content_en
        return self.content_fr

    def get_short_description(self, language='fr'):
        """Get short description in specified language with fallback"""
        if language == 'wo' and self.short_description_wo:
            return self.short_description_wo
        elif language == 'en' and self.short_description_en:
            return self.short_description_en
        return self.short_description_fr

    def get_action_steps(self, language='fr'):
        """Get action steps as list in specified language with fallback"""
        if language == 'wo' and self.action_steps_wo:
            steps = self.action_steps_wo
        elif language == 'en' and self.action_steps_en:
            steps = self.action_steps_en
        else:
            steps = self.action_steps_fr

        # Split by newlines and filter empty lines
        return [step.strip() for step in steps.split('\n') if step.strip()]

    def get_tags_list(self):
        """Get tags as list"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def increment_view(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def mark_helpful(self, helpful=True):
        """Mark advice as helpful or not helpful"""
        if helpful:
            self.helpful_count += 1
        else:
            self.not_helpful_count += 1
        self.save(update_fields=['helpful_count', 'not_helpful_count'])


class DecisionTree(models.Model):
    """
    Decision tree for interactive diagnosis/advice
    """
    LANGUAGE_CHOICES = (
        ('fr', 'Français'),
        ('wo', 'Wolof'),
        ('en', 'English'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_fr = models.CharField(max_length=255, verbose_name="Nom (Français)")
    name_wo = models.CharField(max_length=255, blank=True, verbose_name="Nom (Wolof)")
    name_en = models.CharField(max_length=255, blank=True, verbose_name="Name (English)")

    crop = models.ForeignKey(
        'crops.Crop',
        on_delete=models.CASCADE,
        related_name='decision_trees',
        verbose_name="Culture"
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='fr',
        verbose_name="Langue"
    )

    description_fr = models.TextField(verbose_name="Description (Français)")
    description_wo = models.TextField(blank=True, verbose_name="Description (Wolof)")
    description_en = models.TextField(blank=True, verbose_name="Description (English)")

    # Tree structure stored as JSON (TextField for SQLite compatibility)
    tree_structure = models.TextField(
        verbose_name="Structure de l'arbre (JSON)",
        help_text="Structure JSON de l'arbre de décision"
    )

    is_active = models.BooleanField(default=True, verbose_name="Actif")
    usage_count = models.IntegerField(default=0, verbose_name="Nombre d'utilisations")

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='decision_trees',
        verbose_name="Créé par"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "Arbre de décision"
        verbose_name_plural = "Arbres de décision"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name_fr} ({self.crop.name_fr if self.crop else 'No crop'})"

    def get_name(self, language='fr'):
        """Get name in specified language with fallback"""
        if language == 'wo' and self.name_wo:
            return self.name_wo
        elif language == 'en' and self.name_en:
            return self.name_en
        return self.name_fr

    def get_description(self, language='fr'):
        """Get description in specified language with fallback"""
        if language == 'wo' and self.description_wo:
            return self.description_wo
        elif language == 'en' and self.description_en:
            return self.description_en
        return self.description_fr

    def get_tree_structure(self):
        """Parse JSON tree structure"""
        import json
        try:
            return json.loads(self.tree_structure)
        except:
            return {}

    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class UserAdviceInteraction(models.Model):
    """
    Track user interactions with advice for analytics and personalization
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='advice_interactions'
    )
    advice = models.ForeignKey(
        AdviceEntry,
        on_delete=models.CASCADE,
        related_name='user_interactions'
    )

    ACTION_CHOICES = (
        ('view', 'Vue'),
        ('save', 'Sauvegardé'),
        ('helpful', 'Utile'),
        ('not_helpful', 'Pas utile'),
        ('share', 'Partagé'),
    )

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Interaction conseil"
        verbose_name_plural = "Interactions conseils"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['advice', 'action']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.advice.title_fr}"


class SavedAdvice(models.Model):
    """
    User's saved advice for offline access
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_advice'
    )
    advice = models.ForeignKey(
        AdviceEntry,
        on_delete=models.CASCADE,
        related_name='saved_by_users'
    )

    saved_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, verbose_name="Notes personnelles")

    class Meta:
        verbose_name = "Conseil sauvegardé"
        verbose_name_plural = "Conseils sauvegardés"
        unique_together = ['user', 'advice']
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} - {self.advice.title_fr}"


class CropAdvice(models.Model):
    """
    Structured agricultural advice for each crop
    Follows consistent format: planting season, maturity time, challenges, tips, materials
    Designed for offline access and easy admin management
    """
    LANGUAGE_CHOICES = (
        ('fr', 'Français'),
        ('wo', 'Wolof'),
        ('en', 'English'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    crop = models.OneToOneField(
        'crops.Crop',
        on_delete=models.CASCADE,
        related_name='structured_advice',
        verbose_name="Culture"
    )

    # SECTION 1: PLANTING SEASON
    planting_season_fr = models.TextField(
        verbose_name="Saison de plantation (Français)",
        help_text="Meilleures périodes pour planter cette culture"
    )
    planting_season_wo = models.TextField(
        blank=True,
        verbose_name="Saison de plantation (Wolof)"
    )
    planting_season_en = models.TextField(
        blank=True,
        verbose_name="Planting Season (English)"
    )

    # SECTION 2: MATURITY TIME
    maturity_time_fr = models.TextField(
        verbose_name="Durée de maturation (Français)",
        help_text="Temps nécessaire pour la culture jusqu'à la récolte"
    )
    maturity_time_wo = models.TextField(
        blank=True,
        verbose_name="Durée de maturation (Wolof)"
    )
    maturity_time_en = models.TextField(
        blank=True,
        verbose_name="Maturity Time (English)"
    )

    # SECTION 2B: SOIL TYPE RECOMMENDATIONS
    soil_type_fr = models.TextField(
        default="Tous types de sol adaptés avec bonne préparation",
        verbose_name="Types de sol recommandés (Français)",
        help_text="Types de sol adaptés pour cette culture"
    )
    soil_type_wo = models.TextField(
        blank=True,
        default="",
        verbose_name="Types de sol recommandés (Wolof)"
    )
    soil_type_en = models.TextField(
        blank=True,
        default="",
        verbose_name="Recommended Soil Types (English)"
    )

    # SECTION 3: GROWTH CHALLENGES
    challenges_insects_fr = models.TextField(
        verbose_name="Insectes nuisibles (Français)",
        help_text="Insectes qui attaquent cette culture"
    )
    challenges_insects_wo = models.TextField(
        blank=True,
        verbose_name="Insectes nuisibles (Wolof)"
    )
    challenges_insects_en = models.TextField(
        blank=True,
        verbose_name="Pest Insects (English)"
    )

    challenges_diseases_fr = models.TextField(
        verbose_name="Maladies courantes (Français)",
        help_text="Maladies qui affectent cette culture"
    )
    challenges_diseases_wo = models.TextField(
        blank=True,
        verbose_name="Maladies courantes (Wolof)"
    )
    challenges_diseases_en = models.TextField(
        blank=True,
        verbose_name="Common Diseases (English)"
    )

    challenges_environmental_fr = models.TextField(
        verbose_name="Problèmes environnementaux (Français)",
        help_text="Sécheresse, inondations, etc."
    )
    challenges_environmental_wo = models.TextField(
        blank=True,
        verbose_name="Problèmes environnementaux (Wolof)"
    )
    challenges_environmental_en = models.TextField(
        blank=True,
        verbose_name="Environmental Issues (English)"
    )

    # SECTION 4: PRACTICAL TIPS
    prevention_tips_fr = models.TextField(
        verbose_name="Conseils de prévention (Français)",
        help_text="Comment prévenir les problèmes"
    )
    prevention_tips_wo = models.TextField(
        blank=True,
        verbose_name="Conseils de prévention (Wolof)"
    )
    prevention_tips_en = models.TextField(
        blank=True,
        verbose_name="Prevention Tips (English)"
    )

    management_tips_fr = models.TextField(
        verbose_name="Conseils de gestion (Français)",
        help_text="Comment gérer les problèmes existants"
    )
    management_tips_wo = models.TextField(
        blank=True,
        verbose_name="Conseils de gestion (Wolof)"
    )
    management_tips_en = models.TextField(
        blank=True,
        verbose_name="Management Tips (English)"
    )

    # SECTION 5: RECOMMENDED MATERIALS
    recommended_fertilizers_fr = models.TextField(
        verbose_name="Engrais recommandés (Français)",
        help_text="Types et quantités d'engrais"
    )
    recommended_fertilizers_wo = models.TextField(
        blank=True,
        verbose_name="Engrais recommandés (Wolof)"
    )
    recommended_fertilizers_en = models.TextField(
        blank=True,
        verbose_name="Recommended Fertilizers (English)"
    )

    recommended_pesticides_fr = models.TextField(
        verbose_name="Pesticides recommandés (Français)",
        help_text="Produits pour contrôler les ravageurs"
    )
    recommended_pesticides_wo = models.TextField(
        blank=True,
        verbose_name="Pesticides recommandés (Wolof)"
    )
    recommended_pesticides_en = models.TextField(
        blank=True,
        verbose_name="Recommended Pesticides (English)"
    )

    recommended_tools_fr = models.TextField(
        verbose_name="Outils recommandés (Français)",
        help_text="Outils et équipements nécessaires"
    )
    recommended_tools_wo = models.TextField(
        blank=True,
        verbose_name="Outils recommandés (Wolof)"
    )
    recommended_tools_en = models.TextField(
        blank=True,
        verbose_name="Recommended Tools (English)"
    )

    innovative_inputs_fr = models.TextField(
        verbose_name="Intrants innovants (Français)",
        help_text="Nouvelles techniques et produits pour améliorer le rendement"
    )
    innovative_inputs_wo = models.TextField(
        blank=True,
        verbose_name="Intrants innovants (Wolof)"
    )
    innovative_inputs_en = models.TextField(
        blank=True,
        verbose_name="Innovative Inputs (English)"
    )

    # ADDITIONAL FIELDS
    additional_notes_fr = models.TextField(
        blank=True,
        verbose_name="Notes supplémentaires (Français)",
        help_text="Autres informations importantes"
    )
    additional_notes_wo = models.TextField(
        blank=True,
        verbose_name="Notes supplémentaires (Wolof)"
    )
    additional_notes_en = models.TextField(
        blank=True,
        verbose_name="Additional Notes (English)"
    )

    # Metadata
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    view_count = models.IntegerField(default=0, verbose_name="Nombre de vues")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_crop_advice',
        verbose_name="Créé par"
    )

    class Meta:
        verbose_name = "Conseil de culture structuré"
        verbose_name_plural = "Conseils de culture structurés"
        ordering = ['crop__name_fr']

    def __str__(self):
        return f"Conseil pour {self.crop.name_fr}"

    def get_field_value(self, field_base, language='fr'):
        """
        Get field value in specified language with fallback
        field_base examples: 'planting_season', 'maturity_time', etc.
        """
        field_name = f"{field_base}_{language}"
        value = getattr(self, field_name, '')

        # Fallback to French if requested language is empty
        if not value and language != 'fr':
            field_name = f"{field_base}_fr"
            value = getattr(self, field_name, '')

        return value

    def increment_view(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def get_all_advice_data(self, language='fr'):
        """
        Get all advice data in specified language as structured dict
        """
        return {
            'crop': {
                'id': self.crop.id,
                'name': self.crop.name_fr if language == 'fr' else self.crop.name_wo,
                'scientific_name': self.crop.scientific_name,
                'category': self.crop.category,
            },
            'planting_season': self.get_field_value('planting_season', language),
            'maturity_time': self.get_field_value('maturity_time', language),
            'soil_type': self.get_field_value('soil_type', language),
            'challenges': {
                'insects': self.get_field_value('challenges_insects', language),
                'diseases': self.get_field_value('challenges_diseases', language),
                'environmental': self.get_field_value('challenges_environmental', language),
            },
            'tips': {
                'prevention': self.get_field_value('prevention_tips', language),
                'management': self.get_field_value('management_tips', language),
            },
            'recommended_materials': {
                'fertilizers': self.get_field_value('recommended_fertilizers', language),
                'pesticides': self.get_field_value('recommended_pesticides', language),
                'tools': self.get_field_value('recommended_tools', language),
                'innovative_inputs': self.get_field_value('innovative_inputs', language),
            },
            'additional_notes': self.get_field_value('additional_notes', language),
            'view_count': self.view_count,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }
