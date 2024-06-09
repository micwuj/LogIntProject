from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('home/', include('home.urls')),
    path('sources/', include('sources.urls')),
    path('admin/', admin.site.urls),
    path('history/', include('history.urls')),
    path('reports/', include('reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)