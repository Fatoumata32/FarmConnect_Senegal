# farmconnect_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# URLs non traduites (admin, media, static)
urlpatterns = [
    path('admin/', admin.site.urls),
]

# URLs traduites avec i18n
urlpatterns += i18n_patterns(
    # App principale - ATTENTION: Une seule fois!
    path('', include('farmconnect_app.urls')),
    
    # Authentification Django (optionnel)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Décommentez si ces apps existent
    # path('crops/', include('crops.urls')),
    # path('weather/', include('weather.urls')),
    # path('marketplace/', include('marketplace.urls')),
    
    prefix_default_language=True,
)

# Fichiers statiques et média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)