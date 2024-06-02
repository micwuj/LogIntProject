from django.urls import path
from . import views

urlpatterns = [
    path('emulator', views.emulator, name='emulator'),
]