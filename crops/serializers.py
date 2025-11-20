"""
Serializers pour l'API REST de FarmConnect
Convertit les modèles Django en JSON et vice-versa
"""

from rest_framework import serializers
from .models import Crop, SoilType, Season, CropSoilRecommendation, CropTip
from farmconnect_app.models import User


class SoilTypeSerializer(serializers.ModelSerializer):
    """Serializer pour les types de sol"""

    texture_display = serializers.CharField(source='get_texture_display', read_only=True)
    drainage_display = serializers.CharField(source='get_drainage_display', read_only=True)
    fertility_display = serializers.CharField(source='get_fertility_display', read_only=True)
    water_retention_display = serializers.CharField(source='get_water_retention_display', read_only=True)
    organic_matter_display = serializers.CharField(source='get_organic_matter_display', read_only=True)

    class Meta:
        model = SoilType
        fields = [
            'id', 'name_fr', 'name_wo', 'description_fr', 'description_wo',
            'ph_min', 'ph_max', 'texture', 'texture_display', 'drainage',
            'drainage_display', 'fertility', 'fertility_display',
            'water_retention', 'water_retention_display', 'organic_matter',
            'organic_matter_display', 'created_at'
        ]


class SeasonSerializer(serializers.ModelSerializer):
    """Serializer pour les saisons agricoles"""

    class Meta:
        model = Season
        fields = [
            'id', 'name_fr', 'name_wo', 'start_month', 'end_month',
            'description_fr', 'description_wo'
        ]


class CropTipSerializer(serializers.ModelSerializer):
    """Serializer pour les conseils agricoles"""

    crop_name = serializers.CharField(source='crop.name_fr', read_only=True)
    tip_type_display = serializers.CharField(source='get_tip_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = CropTip
        fields = [
            'id', 'crop', 'crop_name', 'title_fr', 'title_wo',
            'content_fr', 'content_wo', 'tip_type', 'tip_type_display',
            'season', 'is_urgent', 'priority', 'priority_display',
            'created_at', 'updated_at'
        ]


class CropListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des cultures"""

    category_display = serializers.CharField(source='get_category_display', read_only=True)
    water_requirement_display = serializers.CharField(source='get_water_requirement_display', read_only=True)
    suitable_soil_types_count = serializers.SerializerMethodField()

    class Meta:
        model = Crop
        fields = [
            'id', 'name_fr', 'name_wo', 'scientific_name', 'category',
            'category_display', 'growing_season', 'planting_period',
            'harvest_period', 'image', 'water_requirement',
            'water_requirement_display', 'growth_duration_days',
            'drought_resistant', 'flood_tolerant', 'is_active',
            'suitable_soil_types_count'
        ]

    def get_suitable_soil_types_count(self, obj):
        return obj.suitable_soil_types.count()


class CropDetailSerializer(serializers.ModelSerializer):
    """Serializer complet pour les détails d'une culture"""

    category_display = serializers.CharField(source='get_category_display', read_only=True)
    water_requirement_display = serializers.CharField(source='get_water_requirement_display', read_only=True)

    # Relations
    suitable_soil_types = SoilTypeSerializer(many=True, read_only=True)
    suitable_soil_types_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SoilType.objects.all(),
        write_only=True,
        source='suitable_soil_types'
    )

    tips = CropTipSerializer(many=True, read_only=True)

    class Meta:
        model = Crop
        fields = [
            'id', 'name_fr', 'name_wo', 'scientific_name', 'category',
            'category_display', 'growing_season', 'planting_period',
            'harvest_period', 'description_fr', 'description_wo',
            'image', 'is_active', 'created_at',

            # Types de sol
            'suitable_soil_types', 'suitable_soil_types_ids',

            # Besoins climatiques
            'water_requirement', 'water_requirement_display',
            'min_temperature', 'max_temperature', 'optimal_temperature',
            'min_rainfall', 'max_rainfall',

            # Cycle de culture
            'growth_duration_days',

            # Résistance
            'drought_resistant', 'flood_tolerant',

            # Altitude
            'min_altitude', 'max_altitude',

            # Espacement
            'row_spacing_cm', 'plant_spacing_cm',

            # Rendement
            'average_yield',

            # Relations
            'tips'
        ]


class CropSoilRecommendationSerializer(serializers.ModelSerializer):
    """Serializer pour les recommandations culture-sol"""

    crop_name_fr = serializers.CharField(source='crop.name_fr', read_only=True)
    crop_name_wo = serializers.CharField(source='crop.name_wo', read_only=True)
    soil_type_name_fr = serializers.CharField(source='soil_type.name_fr', read_only=True)
    soil_type_name_wo = serializers.CharField(source='soil_type.name_wo', read_only=True)
    season_name_fr = serializers.CharField(source='season.name_fr', read_only=True, allow_null=True)
    season_name_wo = serializers.CharField(source='season.name_wo', read_only=True, allow_null=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = CropSoilRecommendation
        fields = [
            'id', 'crop', 'crop_name_fr', 'crop_name_wo',
            'soil_type', 'soil_type_name_fr', 'soil_type_name_wo',
            'season', 'season_name_fr', 'season_name_wo',

            # Recommandations
            'soil_preparation_fr', 'soil_preparation_wo',
            'fertilization_fr', 'fertilization_wo',
            'irrigation_fr', 'irrigation_wo',
            'pest_management_fr', 'pest_management_wo',
            'harvest_advice_fr', 'harvest_advice_wo',
            'storage_advice_fr', 'storage_advice_wo',
            'recommended_amendments_fr', 'recommended_amendments_wo',

            # Espacement et rendement
            'recommended_row_spacing', 'recommended_plant_spacing',
            'expected_yield',

            # Conditions et précautions
            'optimal_conditions_fr', 'optimal_conditions_wo',
            'warnings_fr', 'warnings_wo',

            # Métadonnées
            'priority', 'priority_display', 'is_active',
            'created_at', 'updated_at'
        ]


class CropSoilRecommendationListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des recommandations"""

    crop_name = serializers.CharField(source='crop.name_fr', read_only=True)
    soil_type_name = serializers.CharField(source='soil_type.name_fr', read_only=True)
    season_name = serializers.CharField(source='season.name_fr', read_only=True, allow_null=True)

    class Meta:
        model = CropSoilRecommendation
        fields = [
            'id', 'crop', 'crop_name', 'soil_type', 'soil_type_name',
            'season', 'season_name', 'expected_yield', 'priority', 'is_active'
        ]
