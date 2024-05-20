from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('integration', views.add_integration, name='integration'),
    path('integration<int:integration_id>', views.integration_details, name='integration_details'),
    path('integration<int:integration_id>/integrationedit', views.edit_integration, name='edit_integration'),
    path('integration<int:integration_id>/add', views.add_driver_account, name='integration_add_driver'),
]