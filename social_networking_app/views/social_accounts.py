from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework import generics
from rest_framework import pagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..constants.enums import ListUserEnum
from ..constants.messages import FRIEND_EMAIL_NOT_FOUND
from ..constants.messages import FRIEND_REQUEST_ACCEPTED
from ..constants.messages import FRIEND_REQUEST_DECLINED
from ..constants.messages import FRIEND_REQUEST_NOT_FOUND
from ..constants.messages import FRIEND_REQUEST_SENT
from ..models import FriendRequest
from ..models import User
from ..serializers.social_accounts import FriendRequestSerializer
from ..serializers.social_accounts import ListUserSerializer
from social_networking_media.decorators import manual_params


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=manual_params(
            params=["list_friends"], enums=ListUserEnum, description="some description"
        )
    ),
)
class ListUserView(generics.ListAPIView):
    """
    API endpoint for retrieving a list of users.

    This view allows authenticated users to search and filter through a list of active users.
    It utilizes ListUserSerializer for data serialization and offers pagination for extensive user lists.

    - Filtering by name and email is enabled using SearchFilter.
    - Users can retrieve their friend list by setting the "list_friends" query parameter to True.

    - Permission classes:
        - IsAuthenticated: Only authenticated users can access this endpoint.
    """

    serializer_class = ListUserSerializer
    queryset = User.objects.all()  # Use .all() for base queryset
    filter_backends = [filters.SearchFilter]  # Enable search filtering (optional)
    search_fields = ["name", "email"]  # Fields to search by (optional)
    pagination_class = pagination.PageNumberPagination  # Enable pagination
    permission_classes = [IsAuthenticated]  # authentication class

    def get_queryset(self):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        Filters the queryset based on request parameters.

        - Returns all active users by default.
        - Filters for the authenticated user's friends if "list_friends" is set to True.
        - Excludes the requesting user, staff users, and superusers from the list.
        """
        queryset = super().get_queryset()  # Use parent class's base queryset
        queryset = queryset.filter(is_active=True)
        if (
            self.request.query_params.get("list_friends")
            == ListUserEnum.list_friends_only.value
        ):
            queryset = queryset.filter(
                requests_received__sender=self.request.user,
                requests_received__status="accepted",
            )
        elif (
            self.request.query_params.get("list_friends")
            == ListUserEnum.list_full_users.value
        ):
            queryset = queryset.exclude(
                email=self.request.user, is_superuser=True, is_staff=True
            )
        return queryset


class FriendRequestView(APIView):
    """
    API endpoint for managing friend requests.

    This view provides functionalities for authenticated users to:

    - Retrieve a list of their pending friend requests (GET method).
    - Send a friend request to another user (POST method).
    - Accept or decline a pending friend request (PUT method).

    - Permission classes:
        - IsAuthenticated: Only authenticated users can access this endpoint.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves a list of pending friend requests for the authenticated user.

        - Filters FriendRequest objects to include only those where the receiver is the
          requesting user and the status is "pending".
        - Serializes the retrieved friend requests using FriendRequestSerializer.
        - Returns a JSON response with the serialized data and a 200 OK status code.
        """
        user = request.user
        friend_requests = FriendRequest.objects.filter(receiver=user, status="pending")
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO:some bugs to fix:-only getting "Your daily limit has been exceeded." message
    def post(self, request):
        """
        Sends a friend request to another user.

        - Extracts data from the request body.
        - Updates the data with the sender's email (authenticated user).
        - Creates a FriendRequestSerializer instance with the updated data and request context.
        - Validates the serializer data.
        - If validation fails, returns a JSON response with validation errors and a 400 Bad Request status code.
        - If validation is successful, saves the FriendRequest object and returns a JSON response
          with a success message and a 201 Created status code.
        """
        data = request.data
        data.update({"sender": request.user.email})
        serializer = FriendRequestSerializer(data=data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            {"message": FRIEND_REQUEST_SENT}, status=status.HTTP_201_CREATED
        )

    def put(self, request, pk):
        """
        Updates the status of a friend request (accept or decline).

        - Attempts to retrieve a FriendRequest object with the provided primary key (pk).
        - Handles the case where the FriendRequest is not found and returns a JSON response
          with an error message and a 404 Not Found status code.
        - Extracts data from the request body.
        - Creates a FriendRequestSerializer instance with the retrieved FriendRequest object,
          updated data, request context, and partial update enabled.
        - Validates the serializer data.
        - If validation fails, returns a JSON response with validation errors and a 400 Bad Request status code.
        - If validation is successful, saves the updated FriendRequest object.
        - Checks the updated status and returns a JSON response with an appropriate success message
          and a 200 OK status code based on whether the request was accepted or declined.
        """
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response(
                {"error": FRIEND_REQUEST_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        serializer = FriendRequestSerializer(
            friend_request,
            data=data,
            partial=True,
            context={
                "request": request,
                "sender": request.user.email,
                "id": pk,
                "status": data.get("status"),
            },
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        if data.get("status") == "accepted":
            return Response(
                {"message": FRIEND_REQUEST_ACCEPTED}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": FRIEND_REQUEST_DECLINED}, status=status.HTTP_200_OK
            )
