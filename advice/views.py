from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import AdviceEntry, DecisionTree, SavedAdvice, UserAdviceInteraction, CropAdvice
from .serializers import (
    AdviceEntryListSerializer,
    AdviceEntryDetailSerializer,
    DecisionTreeSerializer,
    SavedAdviceSerializer,
    UserAdviceInteractionSerializer,
    CropAdviceSerializer,
    CropWithAdviceSerializer
)
from crops.models import Crop


# Template views
def advice_library(request):
    """Main advice library page"""
    return render(request, 'advice/library.html')


def crop_advice_guide(request):
    """Crop advice guide page with clickable crop buttons"""
    return render(request, 'advice/crop_advice_guide.html')


class AdviceEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for browsing and retrieving advice entries.

    list: Get all active advice entries with filtering
    retrieve: Get detailed advice entry
    search: Search advice by query
    by_crop: Get advice for specific crop
    categories: Get all available categories
    mark_helpful: Mark advice as helpful/not helpful
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['crop', 'category', 'stage', 'severity', 'is_featured']
    search_fields = ['title_fr', 'title_wo', 'title_en', 'content_fr', 'tags']
    ordering_fields = ['priority', 'created_at', 'view_count', 'helpful_count']
    ordering = ['-priority', '-created_at']

    def get_queryset(self):
        """Return only active advice entries"""
        return AdviceEntry.objects.filter(is_active=True).select_related('crop', 'author')

    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'retrieve':
            return AdviceEntryDetailSerializer
        return AdviceEntryListSerializer

    def get_serializer_context(self):
        """Add language to serializer context"""
        context = super().get_serializer_context()
        # Get language from query params, default to French
        context['language'] = self.request.query_params.get('lang', 'fr')
        return context

    def retrieve(self, request, *args, **kwargs):
        """Retrieve advice and increment view count"""
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search advice entries by query string.
        Query params: q (search query), lang (language)
        """
        query = request.query_params.get('q', '').strip()
        language = request.query_params.get('lang', 'fr')

        if not query:
            return Response({'error': 'Search query required'}, status=status.HTTP_400_BAD_REQUEST)

        # Search in title, content, and tags based on language
        queryset = self.get_queryset()

        if language == 'wo':
            queryset = queryset.filter(
                Q(title_wo__icontains=query) |
                Q(content_wo__icontains=query) |
                Q(tags__icontains=query)
            )
        elif language == 'en':
            queryset = queryset.filter(
                Q(title_en__icontains=query) |
                Q(content_en__icontains=query) |
                Q(tags__icontains=query)
            )
        else:  # French (default)
            queryset = queryset.filter(
                Q(title_fr__icontains=query) |
                Q(content_fr__icontains=query) |
                Q(tags__icontains=query)
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_crop(self, request):
        """
        Get advice entries for a specific crop.
        Query params: crop_id, category (optional), stage (optional)
        """
        crop_id = request.query_params.get('crop_id')
        if not crop_id:
            return Response({'error': 'crop_id required'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(crop_id=crop_id)

        # Optional filters
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        stage = request.query_params.get('stage')
        if stage:
            queryset = queryset.filter(stage=stage)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all available categories with counts"""
        from .models import CATEGORY_CHOICES

        categories = []
        for category_key, category_name in CATEGORY_CHOICES:
            count = self.get_queryset().filter(category=category_key).count()
            categories.append({
                'key': category_key,
                'name': category_name,
                'count': count
            })

        return Response(categories)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_helpful(self, request, pk=None):
        """
        Mark advice as helpful or not helpful.
        Request body: {"helpful": true/false}
        """
        advice = self.get_object()
        is_helpful = request.data.get('helpful', True)

        # Update count
        if is_helpful:
            advice.helpful_count += 1
        else:
            advice.not_helpful_count += 1
        advice.save()

        # Record interaction
        UserAdviceInteraction.objects.create(
            user=request.user,
            advice=advice,
            action='helpful' if is_helpful else 'not_helpful'
        )

        return Response({
            'helpful_count': advice.helpful_count,
            'not_helpful_count': advice.not_helpful_count
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def save(self, request, pk=None):
        """
        Save advice for offline access.
        Request body: {"notes": "optional notes"}
        """
        advice = self.get_object()
        notes = request.data.get('notes', '')

        # Create or update saved advice
        saved_advice, created = SavedAdvice.objects.get_or_create(
            user=request.user,
            advice=advice,
            defaults={'notes': notes}
        )

        if not created:
            saved_advice.notes = notes
            saved_advice.save()

        # Record interaction
        UserAdviceInteraction.objects.create(
            user=request.user,
            advice=advice,
            action='save',
            notes=notes
        )

        return Response({
            'saved': True,
            'message': 'Advice saved successfully'
        })


class DecisionTreeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for decision trees.

    list: Get all active decision trees
    retrieve: Get specific decision tree with full structure
    """
    queryset = DecisionTree.objects.filter(is_active=True).select_related('crop')
    serializer_class = DecisionTreeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['crop', 'language']

    def get_serializer_context(self):
        """Add language to serializer context"""
        context = super().get_serializer_context()
        context['language'] = self.request.query_params.get('lang', 'fr')
        return context

    def retrieve(self, request, *args, **kwargs):
        """Retrieve decision tree and increment usage count"""
        instance = self.get_object()
        instance.usage_count += 1
        instance.save(update_fields=['usage_count'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SavedAdviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user's saved advice.

    list: Get all saved advice for current user
    create: Save new advice
    destroy: Remove saved advice
    """
    serializer_class = SavedAdviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only current user's saved advice"""
        return SavedAdvice.objects.filter(user=self.request.user).select_related('advice', 'advice__crop')

    def perform_create(self, serializer):
        """Set user automatically"""
        serializer.save(user=self.request.user)


# Weather-based advice recommendation
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from weather.models import WeatherData


@api_view(['GET'])
@permission_classes([AllowAny])
def weather_based_advice(request):
    """
    Get advice recommendations based on current weather conditions.
    Query params: region (required), crop_id (optional)
    """
    region = request.query_params.get('region')
    crop_id = request.query_params.get('crop_id')
    language = request.query_params.get('lang', 'fr')

    if not region:
        return Response(
            {'error': 'Region parameter required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Get latest weather data for region
        weather = WeatherData.objects.filter(region=region).order_by('-recorded_at').first()

        if not weather:
            return Response(
                {'error': 'No weather data available for this region'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Build queryset based on weather conditions
        queryset = AdviceEntry.objects.filter(is_active=True)

        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)

        # Weather-based recommendations logic
        recommendations = []

        # High temperature advice
        if weather.temperature > 35:
            hot_advice = queryset.filter(
                Q(category='watering') | Q(tags__icontains='chaleur')
            ).order_by('-priority')[:5]
            recommendations.extend(hot_advice)

        # Rain-related advice
        if weather.rain_1h and weather.rain_1h > 0:
            rain_advice = queryset.filter(
                Q(category='disease') | Q(tags__icontains='pluie')
            ).order_by('-priority')[:5]
            recommendations.extend(rain_advice)

        # Low humidity advice
        if weather.humidity < 30:
            dry_advice = queryset.filter(
                Q(category='watering') | Q(tags__icontains='sécheresse')
            ).order_by('-priority')[:5]
            recommendations.extend(dry_advice)

        # High wind advice
        if weather.wind_speed and weather.wind_speed > 20:
            wind_advice = queryset.filter(
                Q(category='weather') | Q(tags__icontains='vent')
            ).order_by('-priority')[:5]
            recommendations.extend(wind_advice)

        # Remove duplicates
        seen = set()
        unique_recommendations = []
        for advice in recommendations:
            if advice.id not in seen:
                seen.add(advice.id)
                unique_recommendations.append(advice)

        # Serialize results
        serializer = AdviceEntryListSerializer(
            unique_recommendations,
            many=True,
            context={'language': language}
        )

        return Response({
            'weather': {
                'region': weather.region,
                'temperature': weather.temperature,
                'humidity': weather.humidity,
                'rain': weather.rain_1h or 0,
                'wind_speed': weather.wind_speed or 0,
                'description': weather.description or '',
                'recorded_at': weather.recorded_at
            },
            'recommendations': serializer.data
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class CropAdviceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for structured crop advice.

    list: Get all crops with structured advice (clickable buttons view)
    retrieve: Get detailed advice for a specific crop
    """
    queryset = CropAdvice.objects.filter(is_active=True).select_related('crop')
    serializer_class = CropAdviceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['crop__category']

    def get_serializer_context(self):
        """Add request to context for language support"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def retrieve(self, request, *args, **kwargs):
        """Retrieve crop advice and increment view count"""
        instance = self.get_object()
        instance.increment_view()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def crops_with_advice(self, request):
        """
        Get list of all crops that have structured advice available.
        Used for displaying crop buttons in the UI.
        Query params: category (optional)
        """
        # Get all crops that have structured advice
        crops = Crop.objects.filter(
            is_active=True,
            structured_advice__is_active=True
        ).select_related('structured_advice')

        # Optional category filter
        category = request.query_params.get('category')
        if category:
            crops = crops.filter(category=category)

        crops = crops.order_by('category', 'name_fr')

        serializer = CropWithAdviceSerializer(
            crops,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_crop(self, request):
        """
        Get structured advice for a specific crop by crop ID.
        Query params: crop_id (required), lang (optional)
        """
        crop_id = request.query_params.get('crop_id')

        if not crop_id:
            return Response(
                {'error': 'crop_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            advice = CropAdvice.objects.select_related('crop').get(
                crop_id=crop_id,
                is_active=True
            )

            # Increment view count
            advice.increment_view()

            serializer = self.get_serializer(advice)
            return Response(serializer.data)

        except CropAdvice.DoesNotExist:
            return Response(
                {'error': 'No structured advice available for this crop'},
                status=status.HTTP_404_NOT_FOUND
            )
