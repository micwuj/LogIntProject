from django import forms
from .models import Integration

class integrationCreate(forms.ModelForm):
    
    class Meta:
        model = Integration
        fields = '__all__'