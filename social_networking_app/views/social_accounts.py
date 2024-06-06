from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth import authenticate, login
from rest_framework import generics
from ..models import User,FriendRequest
from rest_framework import status
from ..constants.messages import FRIEND_EMAIL_NOT_FOUND,FRIEND_REQUEST_NOT_FOUND,FRIEND_REQUEST_SENT

from ..serializers.authentication import UserSerializer
from ..serializers.social_accounts import FriendRequestSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth import authenticate, login
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from ..serializers.social_accounts import ListUserSerializer  # Replace with your actual serializer

class ListUserView(generics.ListAPIView):
    serializer_class = ListUserSerializer
    queryset = User.objects.none()  # Empty queryset to avoid caching (use .all() or get_queryset() within methods)
    filter_backends = [filters.SearchFilter]  # Enable search filtering (optional)
    search_fields = ['name', 'email']  # Fields to search by (optional)
    pagination_class = PageNumberPagination  # Enable pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter the queryset based on request parameters.
        """
        queryset = User.objects  # Use .all() for base queryset
        queryset = (
            queryset.filter(is_active=True)
        )
        if self.request.query_params.get("list_friends"):
            queryset = queryset.filter(
                is_active=True,
                requests_received__sender=self.request.user,
                requests_received__status="accepted"
            )
        else:
            queryset = (
                queryset.filter(is_active=True)
                .exclude(email=self.request.user)
                .exclude(is_staff=True)
                .exclude(is_superuser=True)
                
            )
            
        return queryset.all()
    
class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can send requests
    
    def get(self, request):
        """
        Retrieves a list of friend requests for the authenticated user.
        """
        # Filter friend requests based on the logged-in user
        user = request.user
        friend_requests = FriendRequest.objects.filter(receiver=user,status="pending")

        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        data.update({"sender": request.user.email})

        serializer = FriendRequestSerializer(data=data, context={'request': request})
        
        # Check if the receiver exists
        try:
            User.objects.get(email=data['receiver_username'])
        except User.DoesNotExist:
            return Response(
                {"error": FRIEND_EMAIL_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":FRIEND_REQUEST_SENT}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response(
                {"error": FRIEND_REQUEST_NOT_FOUND}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        data = request.data

        serializer = FriendRequestSerializer(
            friend_request, 
            data=data, 
            partial=True, 
            context={
                'request': request,
                "sender": request.user.email,
                "id":pk,
                "status":data.get('status')
            }
        )
        # Check if the receiver exists
        try:
            User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": FRIEND_EMAIL_NOT_FOUND}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors, 
            tatus=status.HTTP_400_BAD_REQUEST
        )
    
