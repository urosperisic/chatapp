from django.contrib import admin
from django.urls import path, include
from .views import health_check

urlpatterns = [
    path('panel-x/', admin.site.urls),
    path('api/health/', health_check, name='health_check'),
    path('', include('frontend.urls')),
]