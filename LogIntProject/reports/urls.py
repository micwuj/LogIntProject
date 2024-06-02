from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports, name='reports'),
    path('', views.get_all_reports, name='all_reports'),
]