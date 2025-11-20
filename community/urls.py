from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('community/', views.community_view, name='community'),
    path('api/events/', views.api_events, name='api_events'),
    path('api/market-prices/', views.api_market_prices, name='api_market_prices'),
]