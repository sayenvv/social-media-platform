"""authentication module"""
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..constants.messages import INVALID_CREDENTIALS
from ..constants.messages import USER_CREATED
from ..serializers.authentication import LoginSerializer
from ..serializers.authentication import SignupSerializer
from ..serializers.authentication import UserSerializer


class LoginView(APIView):
    """

    API endpoint for user login.

    This view allows unauthenticated users to attempt login using their email and password.
    It validates the provided credentials using a LoginSerializer and retrieves the user object
    if authentication is successful. A token is then generated and returned in the response
    along with a 200 OK status code.

    On failed authentication, an error message (INVALID_CREDENTIALS) is returned with a 400 Bad Request status code.
    """

    permission_classes = []  # Allow unauthenticated users to login
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """

        Handles POST requests for user login.

        - Validates the request data using the LoginSerializer.
        - Extracts email and password from the validated data.
        - Attempts to authenticate the user using Django's `authenticate` function.
        - If authentication is successful:
            - Creates or retrieves a token for the authenticated user.
            - Returns a response with the token and a 200 OK status code.
        - If authentication fails:
            - Returns a response with an error message and a 400 Bad Request status code.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(
            {"error": INVALID_CREDENTIALS}, status=status.HTTP_400_BAD_REQUEST
        )


class SignupView(APIView):
    """
    API endpoint for user signup.

    This view allows unauthenticated users to register for a new account.
    It validates the signup data using a SignupSerializer and saves the user information
    if validation is successful. A token is then generated and returned in the response
    along with a 201 Created status code and the newly created user's details.

    On failed validation, an exception is raised by the serializer, which will be caught
    and result in a standard error response from Django REST Framework.
    """

    permission_classes = []  # Allow unauthenticated users to signup

    def post(self, request):
        """
        Handles POST requests for user signup.

        - Validates the request data using the SignupSerializer.
        - Saves the user data if validation is successful.
        - Retrieves a token for the newly created user.
        - Returns a response with the token, created user details, and a 201 Created status code.
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Raise exception for invalid data

        user = serializer.save()

        if user:
            token = Token.objects.get(user=user)
            return Response(
                {
                    "message": USER_CREATED,
                    "user": UserSerializer(user).data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
