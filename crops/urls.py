# crops/urls.py (créez ce fichier si il n'existe pas)
from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.crops_list, name='list'),
    path('<int:crop_id>/', views.crop_detail, name='detail'),
    path('api/<int:crop_id>/', views.get_crop_detail_api, name='detail-api'),
    path('tips/', views.farming_tips, name='tips'),
    path('calendar/', views.farming_calendar, name='calendar'),
]


