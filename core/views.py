from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import os


@csrf_exempt
def health_check(request):
    """
    Health check endpoint for monitoring
    Returns server and database status
    Works with both SQLite and PostgreSQL
    """
    db_status = "connected"
    db_version = None
    db_type = "Unknown"
    
    try:
        with connection.cursor() as cursor:
            # Get database engine type
            engine = connection.settings_dict['ENGINE']
            
            if 'postgresql' in engine:
                # PostgreSQL query
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                if version:
                    db_version = version[0]
                    db_type = "PostgreSQL"
            elif 'sqlite' in engine:
                # SQLite query
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()
                if version:
                    db_version = f"SQLite {version[0]}"
                    db_type = "SQLite"
            else:
                # Fallback - just test connection
                cursor.execute("SELECT 1;")
                db_type = engine.split('.')[-1].upper()
                db_version = "Unknown version"
                
    except Exception as e:
        db_status = "disconnected"
        return JsonResponse({
            "status": "error",
            "message": "Health check failed",
            "data": {
                "environment": os.getenv("ENVIRONMENT", "unknown"),
                "database": {
                    "status": db_status,
                    "error": str(e)
                }
            }
        }, status=503)
    
    return JsonResponse({
        "status": "success",
        "message": "Server is healthy",
        "data": {
            "environment": os.getenv("ENVIRONMENT", "unknown"),
            "database": {
                "status": db_status,
                "type": db_type,
                "version": db_version
            }
        }
    })