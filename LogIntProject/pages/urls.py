from django.urls import path
from . import views

urlpatterns = [
    path('emulator', views.emulator, name='emulator'),
    path('reports', views.reports, name='reports'),
    path('sources', views.sources, name='sources'),
]