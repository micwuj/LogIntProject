from django.contrib import admin
from .models import History

class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'operation', 'operation_date')
    list_display_links = ('type', 'name', 'operation', 'operation_date')
    list_filter = ('type', 'operation')

admin.site.register(History, IntegrationAdmin)