from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os

class FrontendAppView(View):
    """
    Serves the compiled React frontend index.html file
    """
    def get(self, request, *args, **kwargs):
        index_path = os.path.join(
            settings.BASE_DIR,
            'frontend',
            'frontend',
            'dist',
            'index.html'
        )
        
        try:
            with open(index_path, encoding='utf-8') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                "Build not found. Run 'npm run build' in frontend/frontend.",
                status=501
            )