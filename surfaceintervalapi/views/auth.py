from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
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
    username = request.data["username"]
    password = request.data["password"]
    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)
    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token, created = Token.objects.get_or_create(user=authenticated_user)
        if created:
            print(f"Token created for user {username}")
        data = {"valid": True, "token": token.key}
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {"valid": False}
    return Response(data)


@extend_schema(
    request=RegisterSerializer,
    responses={200: RegisterTokenSerializer},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    new_user = User.objects.create_user(
        username=request.data["username"],
        email=request.data["email"],
        password=request.data["password"],
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
    )

    diver = Diver.objects.create(
        user=new_user,
        units=request.data["units"],
    )

    token = Token.objects.create(user=diver.user)
    data = {"token": token.key}
    return Response(data)
