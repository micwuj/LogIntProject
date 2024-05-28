from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('integrationdelete', views.home_delete_integration, name='home_delete_integration'),
    path('integration', views.add_integration, name='integration'),
    path('integration<int:integration_id>', views.integration_details, name='integration_details'),
    path('integration<int:integration_id>/integrationedit', views.edit_integration, name='edit_integration'),
    path('integration<int:integration_id>/integrationdelete', views.delete_integration, name='delete_integration'),
    path('integration<int:integration_id>/add', views.add_driver_account, name='add_driver'),
    path('integration<int:integration_id>/edit', views.edit_driver_account, name='edit_driver'),
    path('integration<int:integration_id>/delete', views.delete_driver_account, name='delete_driver'),
]

