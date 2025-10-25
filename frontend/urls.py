from django.urls import re_path
from .views import FrontendAppView

urlpatterns = [
    # Exclude folders and file extensions (with or without trailing slash)
    re_path(
        r'^(?!api/|admin/|assets/|static/)(?!.*\.(js|css|svg|png|jpg|jpeg|gif|ico|woff|woff2|ttf|eot)/?$).*$',
        FrontendAppView.as_view(),
        name='frontend'
    ),
]