from django.urls import path
from . import views

urlpatterns = [
    path('emulator', views.emulator, name='emulator'),
    path('history', views.history, name='history'),
    path('reports', views.reports, name='reports'),
]