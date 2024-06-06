from rest_framework import serializers
from ..models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ..constants.messages import INVALID_CREDENTIALS

class UserSerializer(serializers.ModelSerializer):
  """Serializer for User model"""
  class Meta:
    model = User
    fields = ('id', 'email', 'name', 'phone_number')
    
class LoginSerializer(serializers.Serializer):
  """Serializer for login credentials"""
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True)

  def validate(self, attrs):
    email = attrs.get('email')
    password = attrs.get('password')

    user = User.objects.filter(email=email).first()
    if not user or not user.check_password(password):
      raise serializers.ValidationError(INVALID_CREDENTIALS)
    return attrs


class SignupSerializer(serializers.ModelSerializer):
  """Serializer for user signup (using djoser)"""
  class Meta:
    model = User  # Replace with your User model if different
    fields = ('email', 'name', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  
  def create(self, validated_data):
        """
        Creates a new user instance with the validated data.
        """
        user = User.objects.create_user(
          email=validated_data['email'], 
          password=validated_data['password']
        )
        
        return user
