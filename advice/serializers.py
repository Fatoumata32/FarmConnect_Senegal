from rest_framework import serializers
from .models import AdviceEntry, DecisionTree, SavedAdvice, UserAdviceInteraction, CropAdvice
from crops.models import Crop


class CropSimpleSerializer(serializers.ModelSerializer):
    """Simple crop serializer for nested representation"""
    class Meta:
        model = Crop
        fields = ['id', 'name_fr', 'name_wo']


class AdviceEntryListSerializer(serializers.ModelSerializer):
    """List view serializer - lighter data for browsing"""
    crop = CropSimpleSerializer(read_only=True)
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = AdviceEntry
        fields = [
            'id', 'crop', 'title', 'short_description',
            'category', 'stage', 'severity', 'tags',
            'is_featured', 'priority', 'view_count',
            'helpful_count', 'created_at'
        ]

    def get_title(self, obj):
        """Return title in requested language with fallback"""
        language = self.context.get('language', 'fr')
        return obj.get_title(language)

    def get_short_description(self, obj):
        """Return short description in requested language with fallback"""
        language = self.context.get('language', 'fr')
        return obj.get_short_description(language)


class AdviceEntryDetailSerializer(serializers.ModelSerializer):
    """Detail view serializer - complete data"""
    crop = CropSimpleSerializer(read_only=True)
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    action_steps = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = AdviceEntry
        fields = [
            'id', 'crop', 'title', 'short_description', 'content',
            'action_steps', 'category', 'stage', 'severity', 'tags',
            'is_featured', 'priority', 'view_count', 'helpful_count',
            'not_helpful_count', 'author_name', 'created_at', 'last_updated'
        ]

    def get_title(self, obj):
        language = self.context.get('language', 'fr')
        return obj.get_title(language)

    def get_content(self, obj):
        language = self.context.get('language', 'fr')
        return obj.get_content(language)

    def get_short_description(self, obj):
        language = self.context.get('language', 'fr')
        return obj.get_short_description(language)

    def get_action_steps(self, obj):
        language = self.context.get('language', 'fr')
        steps_text = obj.get_action_steps(language)
        # Split by newlines and return as list
        return [step.strip() for step in steps_text.split('\n') if step.strip()]


class DecisionTreeSerializer(serializers.ModelSerializer):
    """Decision tree serializer"""
    crop = CropSimpleSerializer(read_only=True)
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = DecisionTree
        fields = [
            'id', 'crop', 'name', 'description', 'tree_structure',
            'language', 'is_active', 'usage_count', 'created_at'
        ]

    def get_name(self, obj):
        language = self.context.get('language', 'fr')
        return obj.get_name(language)

    def get_description(self, obj):
        language = self.context.get('language', 'fr')
        return obj.get_description(language)


class SavedAdviceSerializer(serializers.ModelSerializer):
    """Saved advice serializer"""
    advice = AdviceEntryListSerializer(read_only=True)

    class Meta:
        model = SavedAdvice
        fields = ['id', 'advice', 'saved_at', 'last_accessed', 'notes']


class UserAdviceInteractionSerializer(serializers.ModelSerializer):
    """User interaction serializer"""
    class Meta:
        model = UserAdviceInteraction
        fields = ['id', 'advice', 'action', 'timestamp', 'notes']
        read_only_fields = ['timestamp']


class CropAdviceSerializer(serializers.ModelSerializer):
    """
    Serializer for structured crop advice
    Returns advice in language-specific format
    """
    crop_info = serializers.SerializerMethodField()
    advice_data = serializers.SerializerMethodField()

    class Meta:
        model = CropAdvice
        fields = [
            'id', 'crop_info', 'advice_data', 'view_count',
            'last_updated', 'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'view_count', 'last_updated', 'created_at']

    def get_crop_info(self, obj):
        """Get crop basic information"""
        return {
            'id': obj.crop.id,
            'name_fr': obj.crop.name_fr,
            'name_wo': obj.crop.name_wo,
            'scientific_name': obj.crop.scientific_name,
            'category': obj.crop.category,
            'image': obj.crop.image.url if obj.crop.image else None,
        }

    def get_advice_data(self, obj):
        """Get structured advice in requested language"""
        # Get language from request context (default to French)
        request = self.context.get('request')
        language = request.GET.get('lang', 'fr') if request else 'fr'

        return {
            'planting_season': obj.get_field_value('planting_season', language),
            'maturity_time': obj.get_field_value('maturity_time', language),
            'soil_type': obj.get_field_value('soil_type', language),
            'challenges': {
                'insects': obj.get_field_value('challenges_insects', language),
                'diseases': obj.get_field_value('challenges_diseases', language),
                'environmental': obj.get_field_value('challenges_environmental', language),
            },
            'tips': {
                'prevention': obj.get_field_value('prevention_tips', language),
                'management': obj.get_field_value('management_tips', language),
            },
            'recommended_materials': {
                'fertilizers': obj.get_field_value('recommended_fertilizers', language),
                'pesticides': obj.get_field_value('recommended_pesticides', language),
                'tools': obj.get_field_value('recommended_tools', language),
                'innovative_inputs': obj.get_field_value('innovative_inputs', language),
            },
            'additional_notes': obj.get_field_value('additional_notes', language),
        }


class CropWithAdviceSerializer(serializers.ModelSerializer):
    """
    Serializer for crops with their structured advice
    Used in list views showing crops with advice summary
    """
    has_advice = serializers.SerializerMethodField()
    advice_preview = serializers.SerializerMethodField()

    class Meta:
        model = Crop
        fields = [
            'id', 'name_fr', 'name_wo', 'scientific_name', 'category',
            'image', 'has_advice', 'advice_preview'
        ]

    def get_has_advice(self, obj):
        """Check if crop has structured advice"""
        return hasattr(obj, 'structured_advice') and obj.structured_advice.is_active

    def get_advice_preview(self, obj):
        """Get brief preview of advice if available"""
        try:
            advice = obj.structured_advice
            if advice.is_active:
                # Get language from request context
                request = self.context.get('request')
                language = request.GET.get('lang', 'fr') if request else 'fr'

                return {
                    'planting_season_preview': advice.get_field_value('planting_season', language)[:200] + '...',
                    'maturity_time_preview': advice.get_field_value('maturity_time', language)[:150] + '...',
                    'view_count': advice.view_count,
                }
        except:
            pass
        return None
