from django.http import JsonResponse

def success_response(message="Success", data=None, status=200):
    """
    Standard success response format
    Status codes: 200 (OK), 201 (Created), 204 (No Content)
    """
    response = {
        "status": "success",
        "message": message,
    }
    if data is not None:
        response["data"] = data
    
    return JsonResponse(response, status=status)

def error_response(message="Error occurred", errors=None, status=400):
    """
    Standard error response format
    Status codes: 400, 401, 403, 404, 405, 409, 422, 429, 500, 502, 503
    """
    response = {
        "status": "error",
        "message": message,
    }
    if errors is not None:
        response["errors"] = errors
    
    return JsonResponse(response, status=status)

def validation_error_response(errors, message="Validation failed"):
    """
    Validation error (400 Bad Request)
    """
    return error_response(message=message, errors=errors, status=400)

def unauthorized_response(message="Authentication required"):
    """
    Unauthorized access (401)
    """
    return error_response(message=message, status=401)

def forbidden_response(message="Permission denied"):
    """
    Forbidden access (403)
    """
    return error_response(message=message, status=403)

def not_found_response(message="Resource not found"):
    """
    Not found (404)
    """
    return error_response(message=message, status=404)

def conflict_response(message="Resource already exists"):
    """
    Conflict (409) - duplicate resource
    """
    return error_response(message=message, status=409)

def server_error_response(message="Internal server error"):
    """
    Server error (500)
    """
    return error_response(message=message, status=500)