from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('integration', views.integration, name='integration'),
    path('get-integration/<int:integration_id>/', views.get_integration, name='get_integration'),
]