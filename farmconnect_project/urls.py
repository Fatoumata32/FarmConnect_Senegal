from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # APIs REST (sans i18n pour éviter les conflits avec les clients JavaScript)
    path('api/', include('crops.api_urls')),
    path('', include('advice.urls')),  # Advice API endpoints
]

urlpatterns += i18n_patterns(
    path('', include('farmconnect_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
