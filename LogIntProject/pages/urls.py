from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history', views.history, name='history'),
    path('reports', views.reports, name='reports'),
    path('sources', views.sources, name='sources'),
    path('home', views.home, name='home')
]