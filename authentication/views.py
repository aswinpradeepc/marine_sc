# views.py
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from config.settings import GOOGLE_CLIENT_ID
from google.auth.transport import requests

from base.permissions import IsOwner
from .models import User
from .serializers import UserSerializer, LoginSerializer, SignUpSerializer, TokenSerializer, GoogleLoginSerializer

logger = logging.getLogger('authentication')


# Get User API
class UserAPI(viewsets.ModelViewSet):
    """
    A viewset for the User API that allows authenticated users to retrieve and update their own user object.
    """

    # Define the permissions required to access this viewset
    permission_classes = [
        permissions.IsAuthenticated, IsOwner
    ]

    # Set the serializer class used to serialize and deserialize user data
    serializer_class = UserSerializer

    # Define the allowed HTTP methods for this viewset
    http_method_names = ['get', 'put', 'patch']

    # Define the queryset used to retrieve user data
    queryset = User.objects.all()

    def get_object(self):
        """
        Retrieve the user object for the currently authenticated user.
        """
        return self.request.user

    def get_queryset(self):
        """
        Retrieve the queryset of user objects filtered to include only the currently authenticated user.
        """
        return User.objects.filter(id=self.request.user.id)


class Profile(viewsets.ViewSet):
    """
    A viewset for the user profile API that allows authenticated users to retrieve and update their own profile data.
    """

    # Define the permissions required to access this viewset
    permission_classes = [
        permissions.IsAuthenticated, IsOwner
    ]

    # Set the serializer class used to serialize and deserialize user data
    serializer_class = UserSerializer
    parser_class = [FileUploadParser]

    @swagger_auto_schema(responses={200: UserSerializer(many=False)})
    def list(self, request):
        """
        Retrieve the profile data for the currently authenticated user.
        """
        logger.info(f"User {request.user.id} is accessing their profile data.")
        queryset = User.objects.get(id=request.user.id)
        logger.info(
            f"Profile data for user {request.user.id} has been retrieved.")
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: UserSerializer(many=False)})
    def partial_update(self, request):
        """
        Update the profile data for the currently authenticated user.
        """
        logger.info(f"User {request.user.id} is updating their profile data.")
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"Profile data for user {request.user.id} has been updated.",
                extra={
                    'data': serializer.data})
            user.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Log out the currently authenticated user by blacklisting their refresh token.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            try:
                token.blacklist()
            except AttributeError:
                # The token is already blacklisted
                pass

            logger.info(f"User {request.user.id} has been logged out.")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            logger.warning(f"User {request.user.id} is logging out failed.",
                           extra={'data': "Invalid token"})
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                            "message": "Invalid token"})
        except Exception as e:
            logger.warning(f"User {request.user.id} is logging out failed.{type(e)}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Logs in the user with email and password.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            try:
                user = User.objects.filter(email=email).first()
                if user:
                    if user.check_password(password):
                        token = RefreshToken.for_user(user)
                        return Response({
                            'refresh': str(token),
                            'access': str(token.access_token),
                        })
                    else:
                        # Invalid password
                        return Response(
                            status=status.HTTP_401_UNAUTHORIZED, data={
                                "message": "Invalid email or password"})
                else:
                    # User not found with the given email
                    return Response(
                        status=status.HTTP_401_UNAUTHORIZED, data={
                            "message": "Invalid email or password"})
            except Exception as e:
                print(e)
                logger.warning(f"User  is logging in failed.",
                               extra={'data': e})
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:

            logger.warning(f"User  is logging in failed.", extra={
                           'data': "email and password are required"})
            # Invalid request, missing email or password
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                            "message": "email and password are required"})


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request",
                schema=TokenSerializer,
            ),

        },
        swagger_auto_schema=None,

    )
    def create(self, request, *args, **kwargs):
        """
        Creates a new user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user)
        return Response({
            'refresh': str(token),
            'access': str(token.access_token),
        }, status=status.HTTP_201_CREATED)


class GoogleLoginView(generics.GenericAPIView):
    """
    A view for handling user login via Google OAuth2 authentication.
    """

    # Set the serializer class used to serialize and deserialize user data
    serializer_class = GoogleLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Authenticate the user using Google OAuth2 and generate access and refresh tokens.
        """
        # Get the user's Google OAuth2 token from the request data
        logger.info(f"User is logging in.")
        google_key = request.data.get('google_key')

        # If a Google OAuth2 token was provided, attempt to authenticate the user
        if google_key:
            try:
                # Verify the Google OAuth2 token and extract user information
                user_info = id_token.verify_oauth2_token(
                    google_key, requests.Request(),
                    GOOGLE_CLIENT_ID
                )
                logger.warning(f"User {user_info['email']} is trying to logging in.", extra={'data': user_info})

                # Attempt to retrieve an existing user with the authenticated email address
                user = User.objects.filter(email=user_info['email']).first()

                # If a user with the authenticated email exists, generate access and refresh tokens and return them
                if user:
                    logger.warning(f"User {user.get_full_name()} is logging in.")
                    token = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(token),
                        'access': str(token.access_token),
                    })
                # If no user with the authenticated email exists, create a new user and generate access and refresh
                # tokens
                else:
                    logger.warning(f"User {user_info['email']} is logging in for the first time.")
                    user = User.objects.create(
                        email=user_info['email'],
                        full_name=user_info['name'],
                    )

                    token = RefreshToken.for_user(user)

                    return Response({
                        'refresh': str(token),
                        'access': str(token.access_token),
                    })

            # If an exception is raised during authentication, return a bad request response
            except (ValueError,) as e:
                logger.warning(f"User  is logging in failed.", extra={'data': e})
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})
