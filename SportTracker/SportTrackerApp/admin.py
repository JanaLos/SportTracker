from django.contrib import admin
from django.contrib.admin import register
from SportTrackerApp.models import Activity


@register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created', 'km_count']
