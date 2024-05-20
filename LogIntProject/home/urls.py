from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('integration', views.add_integration, name='integration'),
]