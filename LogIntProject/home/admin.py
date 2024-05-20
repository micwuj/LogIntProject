from django.contrib import admin
from .models import Integration, Integration_Account

class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'integration_name', 'integration_date', 'is_active')
    list_display_links = ('id', 'customer', 'integration_name')
    list_filter = ('customer',)
    list_editable = ('is_active',)

admin.site.register(Integration, IntegrationAdmin)
admin.site.register(Integration_Account)