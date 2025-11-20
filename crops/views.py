from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Crop, CropTip, SoilType, CropSoilRecommendation, Season

def crops_list(request):
    crops = Crop.objects.filter(is_active=True).order_by('name_fr')
    recent_tips = CropTip.objects.select_related('crop').order_by('-created_at')[:10]
    
    context = {
        'crops': crops,
        'recent_tips': recent_tips,
    }
    return render(request, 'crops/list.html', context)

def crop_detail(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    tips = CropTip.objects.filter(crop=crop).order_by('-priority', '-created_at')
    
    context = {
        'crop': crop,
        'tips': tips,
    }
    return render(request, 'crops/detail.html', context)

def get_crop_tips_api(request, crop_id):
    language = request.GET.get('lang', 'fr')
    
    try:
        crop = Crop.objects.get(id=crop_id)
        tips = CropTip.objects.filter(crop=crop).order_by('-priority', '-created_at')
        
        tips_data = []
        for tip in tips:
            tips_data.append({
                'title': tip.title_fr if language == 'fr' else tip.title_wo,
                'content': tip.content_fr if language == 'fr' else tip.content_wo,
                'type': tip.tip_type,
                'urgent': tip.is_urgent,
                'priority': tip.priority
            })
        
        return JsonResponse({'tips': tips_data})
    
    except Crop.DoesNotExist:
        return JsonResponse({'error': 'Culture non trouvée'}, status=404)

def get_crop_detail_api(request, crop_id):
    """API pour récupérer les détails complets d'une culture pour le modal"""
    language = request.GET.get('lang', 'fr')

    try:
        crop = Crop.objects.prefetch_related('suitable_soil_types').get(id=crop_id)

        # Récupérer les types de sol appropriés
        soil_types = []
        for soil in crop.suitable_soil_types.all():
            soil_types.append({
                'id': soil.id,
                'name': soil.name_fr if language == 'fr' else soil.name_wo,
                'description': soil.description_fr if language == 'fr' else soil.description_wo,
                'texture': soil.get_texture_display(),
                'drainage': soil.get_drainage_display(),
                'fertility': soil.get_fertility_display()
            })

        # Récupérer les recommandations
        recommendations = []
        crop_recommendations = CropSoilRecommendation.objects.filter(
            crop=crop,
            is_active=True
        ).select_related('soil_type', 'season')[:3]

        for reco in crop_recommendations:
            recommendations.append({
                'soil_type': reco.soil_type.name_fr if language == 'fr' else reco.soil_type.name_wo,
                'season': reco.season.name_fr if language == 'fr' else reco.season.name_wo if reco.season else 'Toutes saisons',
                'soil_preparation': reco.soil_preparation_fr if language == 'fr' else reco.soil_preparation_wo,
                'fertilization': reco.fertilization_fr if language == 'fr' else reco.fertilization_wo,
                'irrigation': reco.irrigation_fr if language == 'fr' else reco.irrigation_wo,
                'pest_management': reco.pest_management_fr if language == 'fr' else reco.pest_management_wo,
                'harvest_advice': reco.harvest_advice_fr if language == 'fr' else reco.harvest_advice_wo,
                'expected_yield': reco.expected_yield
            })

        # Récupérer les conseils
        tips = CropTip.objects.filter(crop=crop).order_by('-priority', '-created_at')[:5]
        tips_data = []
        for tip in tips:
            tips_data.append({
                'title': tip.title_fr if language == 'fr' else tip.title_wo,
                'content': tip.content_fr if language == 'fr' else tip.content_wo,
                'type': tip.get_tip_type_display(),
                'urgent': tip.is_urgent
            })

        # Construire la réponse
        data = {
            'id': crop.id,
            'name': crop.name_fr if language == 'fr' else crop.name_wo,
            'scientific_name': crop.scientific_name,
            'category': crop.get_category_display(),
            'description': crop.description_fr if language == 'fr' else crop.description_wo,
            'image': crop.image.url if crop.image else None,

            # Calendrier
            'growing_season': crop.growing_season,
            'planting_period': crop.planting_period,
            'harvest_period': crop.harvest_period,
            'growth_duration_days': crop.growth_duration_days,

            # Besoins climatiques
            'water_requirement': crop.get_water_requirement_display(),
            'min_temperature': float(crop.min_temperature) if crop.min_temperature else None,
            'max_temperature': float(crop.max_temperature) if crop.max_temperature else None,
            'optimal_temperature': float(crop.optimal_temperature) if crop.optimal_temperature else None,
            'min_rainfall': crop.min_rainfall,
            'max_rainfall': crop.max_rainfall,

            # Caractéristiques
            'drought_resistant': crop.drought_resistant,
            'flood_tolerant': crop.flood_tolerant,
            'row_spacing_cm': crop.row_spacing_cm,
            'plant_spacing_cm': crop.plant_spacing_cm,
            'average_yield': crop.average_yield,
            'min_altitude': crop.min_altitude,
            'max_altitude': crop.max_altitude,

            # Relations
            'soil_types': soil_types,
            'recommendations': recommendations,
            'tips': tips_data
        }

        return JsonResponse(data)

    except Crop.DoesNotExist:
        return JsonResponse({'error': 'Culture non trouvée'}, status=404)

def crop_search(request):
    """Recherche de cultures par nom"""
    query = request.GET.get('q', '')
    if query:
        crops = Crop.objects.filter(
            Q(name_fr__icontains=query) | Q(name_wo__icontains=query)
        ).filter(is_active=True)
    else:
        crops = Crop.objects.filter(is_active=True)

    return render(request, 'crops/search.html', {'crops': crops, 'query': query})

@login_required
def farming_tips(request):
    """Conseils agricoles"""
    tips = CropTip.objects.select_related('crop', 'created_by').order_by('-priority', '-created_at')[:20]
    urgent_tips = tips.filter(is_urgent=True)

    context = {
        'tips': tips,
        'urgent_tips': urgent_tips,
    }
    return render(request, 'crops/tips.html', context)

@login_required
def farming_calendar(request):
    """Calendrier agricole par saison"""
    from datetime import datetime

    current_month = datetime.now().month
    crops = Crop.objects.filter(is_active=True)

    # Grouper les cultures par saison
    calendar_data = {
        'current_month': current_month,
        'crops_by_period': {},
    }

    for crop in crops:
        if crop.planting_period:
            if crop.planting_period not in calendar_data['crops_by_period']:
                calendar_data['crops_by_period'][crop.planting_period] = []
            calendar_data['crops_by_period'][crop.planting_period].append(crop)

    context = {
        'calendar_data': calendar_data,
        'crops': crops,
    }
    return render(request, 'crops/calendar.html', context)
