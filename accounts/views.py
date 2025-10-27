from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, SignupSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from utils.responses import success_response, error_response


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description='Login successful'),
            400: OpenApiResponse(description='Login failed'),
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message='Login failed',
                errors=serializer.errors,
                status=400
            )
        
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return success_response(
            message='Login successful',
            data={
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }
        )
    
class SignupView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=SignupSerializer,
        responses={
            201: OpenApiResponse(description='Account created successfully'),
            400: OpenApiResponse(description='Validation error'),
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message='Signup failed',
                errors=serializer.errors,
                status=400
            )
        
        user = serializer.save()
        
        # Auto-login: generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return success_response(
            message='Account created successfully',
            data={
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            },
            status=201
        )