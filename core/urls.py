from http import HTTPStatus
from django.contrib import admin
from django.urls import path
from django.db import connection
from rest_framework.decorators import api_view
from utils.responses import success_response, error_response
import os


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint for monitoring [MOJ MLADENE]
    """
    db_status = "connected"
    db_type = connection.settings_dict['ENGINE']
    db_version = None
    
    try:
        with connection.cursor() as cursor:
            # Different query based on database type
            if 'postgresql' in db_type:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                db_version = version[0].split(",")[0] if version else "unknown"
                db_name = "PostgreSQL"
            elif 'sqlite' in db_type:
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()
                db_version = f"SQLite {version[0]}" if version else "unknown"
                db_name = "SQLite"
            else:
                cursor.execute("SELECT 1;")
                db_name = "Unknown"
                db_version = "N/A"
                
    except Exception as e:
        return error_response(
            message="Health check failed",
            errors={"database": str(e)},
            status=HTTPStatus.SERVICE_UNAVAILABLE
        )
    
    return success_response(
        message="Server is healthy",
        data={
            "environment": os.getenv("ENVIRONMENT", "development"),
            "database": {
                "status": db_status,
                "type": db_name,
                "version": db_version
            }
        }
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
]