from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('integration', views.add_integration, name='integration'),
    path('integration<int:integration_id>', views.integration_details, name='integration_details'),
]