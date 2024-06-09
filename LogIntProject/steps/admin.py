from django.contrib import admin
from .models import Steps

@admin.register(Steps)
class StepAdmin(admin.ModelAdmin):
    list_display = ('step_number',)