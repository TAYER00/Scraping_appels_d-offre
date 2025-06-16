from django.contrib import admin
from .models import ScrapeJob

@admin.register(ScrapeJob)
class ScrapeJobAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'status', 'run_at')
    list_filter = ('status', 'site_name')
    ordering = ('-run_at',)
    
    def has_add_permission(self, request):
        return False  # Jobs should only be created through the scraper
