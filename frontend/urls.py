from django.urls import re_path
from .views import FrontendAppView

urlpatterns = [
    re_path(r'^(?!assets/|static/).*', FrontendAppView.as_view(), name='frontend'),
]