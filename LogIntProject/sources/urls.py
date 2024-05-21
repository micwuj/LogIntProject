from django.urls import path
from . import views


urlpatterns = [
    path('', views.sources, name='sources'),
    path('add_source', views.add_source, name='add_source'),
    path('edit_source', views.edit_source, name='edit_source'),
    path('delete_source', views.delete_source, name='delete_source')
]