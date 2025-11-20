from django.shortcuts import render
from django.db.models import Avg, Max, Min, Count
from django.http import JsonResponse
from .models import MarketPrice, ForumPost, Event
from crops.models import Crop
from farmconnect_app.models import User
from datetime import date, timedelta


def community_view(request):
    """
    Vue de la communauté avec prix du marché et statistiques réelles
    """
    # Get latest market prices (one per crop, most recent)
    latest_prices = []
    crops_with_prices = MarketPrice.objects.values_list('crop_name', flat=True).distinct()

    for crop in crops_with_prices:
        latest_price = MarketPrice.objects.filter(crop_name=crop).order_by('-date').first()
        if latest_price:
            latest_prices.append(latest_price)

    # Get regional variations for display
    regional_data = []
    for crop in list(crops_with_prices)[:5]:  # Top 5 crops
        crop_prices = MarketPrice.objects.filter(
            crop_name=crop,
            date__gte=date.today() - timedelta(days=7)
        )
        if crop_prices.exists():
            regional_data.append({
                'crop': crop,
                'avg_price': round(crop_prices.aggregate(Avg('price_per_kg'))['price_per_kg__avg'], 2),
                'max_price': round(crop_prices.aggregate(Max('price_per_kg'))['price_per_kg__max'], 2),
                'min_price': round(crop_prices.aggregate(Min('price_per_kg'))['price_per_kg__min'], 2),
                'regions_count': crop_prices.values('region').distinct().count()
            })

    # Stats réelles depuis la base de données
    total_farmers = User.objects.filter(role='farmer', is_active=True).count()
    total_regions = User.objects.values('region').exclude(region='').distinct().count()
    total_crops = Crop.objects.filter(is_active=True).count()
    total_posts = ForumPost.objects.filter(is_active=True).count()

    # Posts récents du forum
    recent_posts = ForumPost.objects.filter(is_active=True).select_related('author').order_by('-created_at')[:5]

    # Upcoming events
    upcoming_events = Event.objects.filter(
        is_active=True,
        date__gte=date.today()
    ).order_by('date', 'start_time')[:5]

    # Total workshops/events
    total_workshops = Event.objects.filter(is_active=True).count()

    context = {
        'latest_prices': latest_prices[:10],  # Top 10 crops
        'regional_data': regional_data,
        'total_farmers': total_farmers,
        'total_regions': total_regions,
        'total_workshops': total_workshops,
        'total_crops': total_crops,
        'total_posts': total_posts,
        'recent_posts': recent_posts,
        'upcoming_events': upcoming_events,
    }

    return render(request, 'farmconnect_app/community.html', context)


def api_events(request):
    """
    API endpoint pour récupérer les événements (pour le calendrier)
    """
    events = Event.objects.filter(is_active=True)

    # Filter by month if provided
    month = request.GET.get('month')
    year = request.GET.get('year')
    if month and year:
        events = events.filter(date__month=int(month), date__year=int(year))

    events_data = []
    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.isoformat(),
            'start_time': event.start_time.strftime('%H:%M'),
            'end_time': event.end_time.strftime('%H:%M') if event.end_time else None,
            'location': event.location,
            'region': event.get_region_display(),
            'event_type': event.event_type,
            'event_type_display': event.get_event_type_display(),
            'event_type_icon': event.get_event_type_icon(),
            'event_type_color': event.get_event_type_color(),
            'organizer': event.organizer,
            'is_free': event.is_free,
            'registration_required': event.registration_required,
            'contact_phone': event.contact_phone,
            'contact_email': event.contact_email,
        })

    return JsonResponse({'events': events_data})


def api_market_prices(request):
    """
    API endpoint pour récupérer les prix du marché
    """
    prices = MarketPrice.objects.all().order_by('-date', 'crop_name')

    # Filter by crop if provided
    crop = request.GET.get('crop')
    if crop:
        prices = prices.filter(crop_name__icontains=crop)

    # Filter by region if provided
    region = request.GET.get('region')
    if region:
        prices = prices.filter(region=region)

    prices_data = []
    for price in prices[:50]:  # Limit to 50 results
        prices_data.append({
            'id': price.id,
            'crop_name': price.crop_name,
            'region': price.region,
            'region_display': price.get_region_display(),
            'price_per_kg': float(price.price_per_kg),
            'date': price.date.isoformat(),
            'trend': price.trend,
            'trend_display': price.get_trend_display(),
            'trend_icon': price.get_trend_icon(),
            'trend_color': price.get_trend_color(),
            'percentage_change': float(price.percentage_change),
        })

    return JsonResponse({'prices': prices_data})