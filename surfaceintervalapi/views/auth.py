from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from surfaceintervalapi.models import Diver
from surfaceintervalapi.serializers import (
    LoginSerializer,
    TokenSerializer,
    RegisterSerializer,
    RegisterTokenSerializer,
)


@extend_schema(
    request=LoginSerializer,
    responses={200: TokenSerializer},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Handles the authentication of a user
    Method arguments:
    request -- The full HTTP request object
    """
    try:
        email = request.data.get("email", "").lower()
        password = request.data.get("password", "")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Check if user is active
        if not user.is_active:
            return Response(
                {"error": "User account is disabled"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Authenticate user
        authenticated_user = authenticate(username=user.username, password=password)
        if authenticated_user is None:
            return Response(
                {"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Update last login
        user.last_login = timezone.now()
        user.save()

        # Generate tokens
        try:
            refresh = RefreshToken.for_user(authenticated_user)
            data = {
                "valid": True,
                "token": str(refresh.access_token),
                "refresh": str(refresh),
            }
            return Response(data, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response(
                {"error": f"Error generating token: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    request=RegisterSerializer,
    responses={200: RegisterTokenSerializer},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    new_user = User.objects.create_user(
        username=request.data["username"],
        email=request.data["email"].lower(),
        password=request.data["password"],
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
    )

    diver = Diver.objects.create(
        user=new_user,
        units=request.data["units"],
    )
    diver.user.last_login = timezone.now()
    diver.user.save()

    refresh = RefreshToken.for_user(diver.user)
    data = {"token": str(refresh.access_token), "refresh": str(refresh)}
    return Response(data)
