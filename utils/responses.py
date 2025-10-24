from http import HTTPStatus
from rest_framework.response import Response


def _build_body(status_str, message, payload=None):
    """
    Helper that creates the basic response structure
    """
    body = {
        "status": status_str,
        "message": message,
    }
    if payload is not None:
        key = "data" if status_str == "success" else "errors"
        body[key] = payload
    return body


# SUCCESS RESPONSES
def success_response(message="Success", data=None, status=HTTPStatus.OK):
    """
    Standard success response
    Status codes: 200 (OK), 201 (Created), 204 (No Content)
    """
    body = _build_body("success", message, data)
    return Response(body, status=status)


# ERROR RESPONSES
def error_response(message="Error occurred", errors=None, status=HTTPStatus.BAD_REQUEST):
    """
    Standard error response
    Status codes: 400, 401, 403, 404, 405, 409, 422, 429, 500, 502, 503
    """
    body = _build_body("error", message, errors)
    return Response(body, status=status)


# COMMON SHORTCUTS
def validation_error_response(errors, message="Validation failed"):
    """400 Bad Request"""
    return error_response(message=message, errors=errors, status=HTTPStatus.BAD_REQUEST)


def unauthorized_response(message="Authentication required"):
    """401 Unauthorized"""
    return error_response(message=message, status=HTTPStatus.UNAUTHORIZED)


def forbidden_response(message="Permission denied"):
    """403 Forbidden"""
    return error_response(message=message, status=HTTPStatus.FORBIDDEN)


def not_found_response(message="Resource not found"):
    """404 Not Found"""
    return error_response(message=message, status=HTTPStatus.NOT_FOUND)


def conflict_response(message="Resource already exists"):
    """409 Conflict"""
    return error_response(message=message, status=HTTPStatus.CONFLICT)


def server_error_response(message="Internal server error"):
    """500 Internal Server Error"""
    return error_response(message=message, status=HTTPStatus.INTERNAL_SERVER_ERROR)