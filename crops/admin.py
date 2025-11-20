from django.contrib import admin
from .models import Crop, CropTip, SoilType, Season, CropSoilRecommendation

@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ('name_fr', 'name_wo', 'texture', 'drainage', 'fertility', 'water_retention')
    list_filter = ('texture', 'drainage', 'fertility', 'water_retention', 'organic_matter')
    search_fields = ('name_fr', 'name_wo', 'description_fr', 'description_wo')
    ordering = ('name_fr',)
    fieldsets = (
        ('Informations générales', {
            'fields': ('name_fr', 'name_wo', 'description_fr', 'description_wo')
        }),
        ('Propriétés chimiques', {
            'fields': ('ph_min', 'ph_max')
        }),
        ('Propriétés physiques', {
            'fields': ('texture', 'drainage', 'fertility', 'water_retention', 'organic_matter')
        }),
    )

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name_fr', 'name_wo', 'start_month', 'end_month')
    ordering = ('start_month',)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name_fr', 'name_wo', 'category', 'growing_season', 'water_requirement', 'drought_resistant', 'is_active', 'created_at')
    list_filter = ('category', 'growing_season', 'is_active', 'water_requirement', 'drought_resistant', 'flood_tolerant')
    search_fields = ('name_fr', 'name_wo', 'scientific_name', 'description_fr')
    ordering = ('name_fr',)
    filter_horizontal = ('suitable_soil_types',)
    # Enable autocomplete for CropAdvice admin
    autocomplete_fields = []
    fieldsets = (
        ('Informations générales', {
            'fields': ('name_fr', 'name_wo', 'scientific_name', 'category', 'description_fr', 'description_wo', 'image', 'is_active')
        }),
        ('Calendrier cultural', {
            'fields': ('growing_season', 'planting_period', 'harvest_period', 'growth_duration_days')
        }),
        ('Besoins climatiques', {
            'fields': ('water_requirement', 'min_temperature', 'max_temperature', 'optimal_temperature', 'min_rainfall', 'max_rainfall')
        }),
        ('Conditions du sol', {
            'fields': ('suitable_soil_types', 'min_altitude', 'max_altitude')
        }),
        ('Résistance', {
            'fields': ('drought_resistant', 'flood_tolerant')
        }),
        ('Techniques culturales', {
            'fields': ('row_spacing_cm', 'plant_spacing_cm', 'average_yield')
        }),
    )

@admin.register(CropTip)
class CropTipAdmin(admin.ModelAdmin):
    list_display = ('title_fr', 'crop', 'tip_type', 'priority', 'is_urgent', 'created_by', 'created_at')
    list_filter = ('tip_type', 'priority', 'is_urgent', 'season', 'crop')
    search_fields = ('title_fr', 'title_wo', 'content_fr', 'content_wo')
    ordering = ('-priority', '-created_at')
    raw_id_fields = ('crop', 'created_by')

@admin.register(CropSoilRecommendation)
class CropSoilRecommendationAdmin(admin.ModelAdmin):
    list_display = ('crop', 'soil_type', 'season', 'priority', 'expected_yield', 'is_active')
    list_filter = ('priority', 'is_active', 'season', 'soil_type', 'crop__category')
    search_fields = ('crop__name_fr', 'soil_type__name_fr', 'soil_preparation_fr', 'fertilization_fr')
    ordering = ('-priority', 'crop__name_fr')
    raw_id_fields = ('crop', 'soil_type', 'season')
    fieldsets = (
        ('Configuration', {
            'fields': ('crop', 'soil_type', 'season', 'priority', 'is_active')
        }),
        ('Préparation du sol', {
            'fields': ('soil_preparation_fr', 'soil_preparation_wo')
        }),
        ('Fertilisation', {
            'fields': ('fertilization_fr', 'fertilization_wo', 'recommended_amendments_fr', 'recommended_amendments_wo')
        }),
        ('Irrigation', {
            'fields': ('irrigation_fr', 'irrigation_wo')
        }),
        ('Protection phytosanitaire', {
            'fields': ('pest_management_fr', 'pest_management_wo')
        }),
        ('Récolte et stockage', {
            'fields': ('harvest_advice_fr', 'harvest_advice_wo', 'storage_advice_fr', 'storage_advice_wo')
        }),
        ('Espacement et rendement', {
            'fields': ('recommended_row_spacing', 'recommended_plant_spacing', 'expected_yield')
        }),
        ('Conditions et précautions', {
            'fields': ('optimal_conditions_fr', 'optimal_conditions_wo', 'warnings_fr', 'warnings_wo')
        }),
    )
