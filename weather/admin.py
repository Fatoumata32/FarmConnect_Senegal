from django.contrib import admin
from .models import WeatherData


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('region', 'temperature', 'humidity', 'description', 'is_current', 'recorded_at')
    list_filter = ('region', 'is_current', 'recorded_at')
    search_fields = ('region', 'description')
    date_hierarchy = 'recorded_at'
    ordering = ('-recorded_at',)

    fieldsets = (
        ('Localisation', {
            'fields': ('region', 'is_current')
        }),
        ('Température', {
            'fields': ('temperature', 'feels_like', 'temp_min', 'temp_max')
        }),
        ('Conditions atmosphériques', {
            'fields': ('humidity', 'pressure', 'cloudiness', 'visibility', 'description', 'icon')
        }),
        ('Vent et précipitations', {
            'fields': ('wind_speed', 'wind_direction', 'rain_1h')
        }),
    )

    readonly_fields = ('timestamp', 'recorded_at')
