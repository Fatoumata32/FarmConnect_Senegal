from django.contrib import admin
from .models import AdviceEntry, DecisionTree, UserAdviceInteraction, SavedAdvice, CropAdvice


@admin.register(AdviceEntry)
class AdviceEntryAdmin(admin.ModelAdmin):
    list_display = ('title_fr', 'crop', 'category', 'stage', 'severity', 'is_active', 'priority', 'view_count')
    list_filter = ('category', 'stage', 'severity', 'is_active', 'is_featured', 'language')
    search_fields = ('title_fr', 'title_wo', 'title_en', 'content_fr', 'tags')
    readonly_fields = ('id', 'created_at', 'last_updated', 'view_count', 'helpful_count', 'not_helpful_count')
    list_editable = ('is_active', 'priority')
    list_per_page = 50

    fieldsets = (
        ('Titres', {
            'fields': ('title_fr', 'title_wo', 'title_en')
        }),
        ('Informations de base', {
            'fields': ('crop', 'category', 'stage', 'severity', 'tags', 'language')
        }),
        ('Descriptions courtes', {
            'fields': ('short_description_fr', 'short_description_wo', 'short_description_en')
        }),
        ('Contenu complet', {
            'fields': ('content_fr', 'content_wo', 'content_en'),
            'classes': ('collapse',)
        }),
        ('Étapes d\'action', {
            'fields': ('action_steps_fr', 'action_steps_wo', 'action_steps_en'),
            'description': 'Une étape par ligne',
            'classes': ('collapse',)
        }),
        ('Paramètres', {
            'fields': ('is_active', 'is_featured', 'priority', 'author', 'version')
        }),
        ('Statistiques', {
            'fields': ('view_count', 'helpful_count', 'not_helpful_count', 'created_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(DecisionTree)
class DecisionTreeAdmin(admin.ModelAdmin):
    list_display = ('name_fr', 'crop', 'language', 'is_active', 'usage_count', 'created_at')
    list_filter = ('language', 'is_active', 'crop')
    search_fields = ('name_fr', 'name_wo', 'name_en', 'description_fr')
    readonly_fields = ('id', 'created_at', 'last_updated', 'usage_count')

    fieldsets = (
        ('Noms', {
            'fields': ('name_fr', 'name_wo', 'name_en')
        }),
        ('Informations de base', {
            'fields': ('crop', 'language', 'is_active')
        }),
        ('Descriptions', {
            'fields': ('description_fr', 'description_wo', 'description_en')
        }),
        ('Structure de l\'arbre', {
            'fields': ('tree_structure',),
            'description': 'Format JSON'
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'usage_count', 'created_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SavedAdvice)
class SavedAdviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'advice', 'saved_at', 'last_accessed')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'advice__title_fr', 'notes')
    readonly_fields = ('id', 'saved_at', 'last_accessed')


@admin.register(UserAdviceInteraction)
class UserAdviceInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'advice', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'advice__title_fr')
    readonly_fields = ('id', 'timestamp')
    date_hierarchy = 'timestamp'


@admin.register(CropAdvice)
class CropAdviceAdmin(admin.ModelAdmin):
    """
    Admin interface for structured crop advice
    Provides easy CRUD operations for managing advice for each crop
    """
    list_display = ('crop', 'is_active', 'view_count', 'last_updated')
    list_filter = ('is_active', 'crop__category')
    search_fields = ('crop__name_fr', 'crop__name_wo', 'planting_season_fr', 'challenges_insects_fr')
    readonly_fields = ('id', 'created_at', 'last_updated', 'view_count')
    list_editable = ('is_active',)
    autocomplete_fields = ['crop']

    fieldsets = (
        ('Culture', {
            'fields': ('crop', 'is_active')
        }),
        ('1. Saison de plantation', {
            'fields': ('planting_season_fr', 'planting_season_wo', 'planting_season_en'),
            'description': 'Meilleures périodes pour planter cette culture'
        }),
        ('2. Durée de maturation', {
            'fields': ('maturity_time_fr', 'maturity_time_wo', 'maturity_time_en'),
            'description': 'Temps nécessaire jusqu\'à la récolte'
        }),
        ('2B. Types de sol recommandés', {
            'fields': ('soil_type_fr', 'soil_type_wo', 'soil_type_en'),
            'description': 'Types de sol adaptés pour cette culture'
        }),
        ('3. Défis - Insectes', {
            'fields': ('challenges_insects_fr', 'challenges_insects_wo', 'challenges_insects_en'),
            'classes': ('collapse',)
        }),
        ('3. Défis - Maladies', {
            'fields': ('challenges_diseases_fr', 'challenges_diseases_wo', 'challenges_diseases_en'),
            'classes': ('collapse',)
        }),
        ('3. Défis - Environnementaux', {
            'fields': ('challenges_environmental_fr', 'challenges_environmental_wo', 'challenges_environmental_en'),
            'classes': ('collapse',)
        }),
        ('4. Conseils - Prévention', {
            'fields': ('prevention_tips_fr', 'prevention_tips_wo', 'prevention_tips_en'),
            'classes': ('collapse',)
        }),
        ('4. Conseils - Gestion', {
            'fields': ('management_tips_fr', 'management_tips_wo', 'management_tips_en'),
            'classes': ('collapse',)
        }),
        ('5. Matériaux - Engrais', {
            'fields': ('recommended_fertilizers_fr', 'recommended_fertilizers_wo', 'recommended_fertilizers_en'),
            'classes': ('collapse',)
        }),
        ('5. Matériaux - Pesticides', {
            'fields': ('recommended_pesticides_fr', 'recommended_pesticides_wo', 'recommended_pesticides_en'),
            'classes': ('collapse',)
        }),
        ('5. Matériaux - Outils', {
            'fields': ('recommended_tools_fr', 'recommended_tools_wo', 'recommended_tools_en'),
            'classes': ('collapse',)
        }),
        ('5. Matériaux - Intrants innovants', {
            'fields': ('innovative_inputs_fr', 'innovative_inputs_wo', 'innovative_inputs_en'),
            'classes': ('collapse',)
        }),
        ('Notes supplémentaires', {
            'fields': ('additional_notes_fr', 'additional_notes_wo', 'additional_notes_en'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'view_count', 'created_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
