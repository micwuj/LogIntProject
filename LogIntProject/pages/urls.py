from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('emulator', views.emulator, name='emulator'),
    path('history', views.history, name='history'),
    path('reports', views.reports, name='reports'),
    path('sources', views.sources, name='sources'),
    path('home', views.home, name='home'),
    path('add_source', views.add_source, name='add_source'),
    path('edit_source', views.edit_source, name='edit_source'),
    path('delete_source', views.delete_source, name='delete_source')
]