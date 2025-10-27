from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, PasswordResetToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    LoginSerializer, SignupSerializer, LogoutSerializer,
    RequestPasswordResetSerializer, ResetPasswordSerializer
)
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
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=LogoutSerializer,
        responses={
            200: OpenApiResponse(description='Logout successful'),
            400: OpenApiResponse(description='Logout failed'),
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message='Logout failed',
                errors=serializer.errors,
                status=400
            )
        
        return success_response(
            message='Logout successful',
            data=None
        )
    
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=RequestPasswordResetSerializer,
        responses={
            200: OpenApiResponse(description='Reset email sent'),
            400: OpenApiResponse(description='Request failed'),
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message='Request failed',
                errors=serializer.errors,
                status=400
            )
        
        email = serializer.validated_data['email']
        
        try:
            user = CustomUser.objects.get(email=email)
            
            # Create reset token
            reset_token = PasswordResetToken.objects.create(user=user)
            
            # Prepare email
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token.token}"
            
            # Send email via Brevo
            send_mail(
                subject='Password Reset Request - ChatApp',
                message=f"""Hello {user.username},

You requested a password reset for your ChatApp account.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
ChatApp Team""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
        except CustomUser.DoesNotExist:
            # Don't reveal that user doesn't exist (security best practice)
            pass
        except Exception as e:
            return error_response(
                message='Failed to send reset email',
                errors={'email': [str(e)]},
                status=400
            )
        
        # Always return success (security best practice)
        return success_response(
            message='If this email exists, a reset link has been sent',
            data=None
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(description='Password reset successful'),
            400: OpenApiResponse(description='Reset failed'),
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message='Reset failed',
                errors=serializer.errors,
                status=400
            )
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            
            if not reset_token.is_valid():
                return error_response(
                    message='Token has expired or already been used',
                    errors=None,
                    status=400
                )
            
            # Reset password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            return success_response(
                message='Password reset successful',
                data=None
            )
            
        except PasswordResetToken.DoesNotExist:
            return error_response(
                message='Invalid token',
                errors=None,
                status=400
            )