from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate

from ..serializers.authentication import UserSerializer, LoginSerializer,SignupSerializer
from ..constants.messages import INVALID_CREDENTIALS,USER_CREATED

class LoginView(APIView):
  """API endpoint for login"""
  permission_classes = []  # Allow unauthenticated users to login
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    user = authenticate(email=email, password=password)
    if user:
      token, _ = Token.objects.get_or_create(user=user)
      return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': INVALID_CREDENTIALS}, status=status.HTTP_400_BAD_REQUEST)



class SignupView(APIView):
  """API endpoint for user signup"""
  permission_classes = []  # Allow unauthenticated users to signup

  def post(self, request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user= serializer.save()
    if user:
      token = Token.objects.get(user=user)
    return Response(
      {'message':USER_CREATED,'user': UserSerializer(user).data,"token":token.key},
      status=status.HTTP_201_CREATED
    )