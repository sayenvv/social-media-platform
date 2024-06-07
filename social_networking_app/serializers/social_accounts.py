from datetime import datetime
from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import serializers

from ..constants.constant_variables import ACCEPTED
from ..constants.constant_variables import MAX_FRIEND_REQUESTS_PER_MINUTE
from ..constants.constant_variables import PENDING
from ..constants.constant_variables import REJECTED
from ..constants.constant_variables import TIME_DELTA_VARIABLE
from ..constants.messages import ALREADY_FRIENDS
from ..constants.messages import FRIEND_REQUEST_DECLINED
from ..constants.messages import FRIEND_REQUEST_LIMIT_EXCEEDED
from ..constants.messages import INVALID_FRIEND_REQUEST
from ..constants.messages import REQUEST_ALREADY_SENT
from ..models import FriendRequest
from ..models import User


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "phone_number")


class FriendRequestSerializer(serializers.ModelSerializer):
    receiver_username = serializers.CharField(
        source="receiver.email"
    )  # Show receiver username
    sender = serializers.CharField(source="sender.email")  # Show sender username

    class Meta:
        model = FriendRequest
        fields = ("id", "sender", "receiver_username", "status", "created_at")
        read_only_fields = (
            "sender",
            "status",
            "created_at",
        )  # Sender and status are set automatically

    def validate(self, data):
        friend_request = FriendRequest.objects
        if not self.context.get("id"):
            request_user = self.context["request"].user

            # Check if user is trying to send a request to themselves
            if request_user.email == data["receiver"]["email"]:
                raise serializers.ValidationError(INVALID_FRIEND_REQUEST)
            one_minute_ago = datetime.now() - timedelta(minutes=TIME_DELTA_VARIABLE)

            friend_request_count = friend_request.filter(
                sender=request_user,
                created_at__gte=one_minute_ago,
                created_at__lte=datetime.now(),
            ).aggregate(count=Count("*"))["count"]

            if friend_request_count <= MAX_FRIEND_REQUESTS_PER_MINUTE:
                raise serializers.ValidationError(FRIEND_REQUEST_LIMIT_EXCEEDED)
            # Check if a pending request already exists
            if friend_request.filter(
                sender=request_user,
                receiver__email=data["receiver"]["email"],
                status=PENDING,
            ).exists():
                raise serializers.ValidationError(REQUEST_ALREADY_SENT)

            elif friend_request.filter(
                sender=request_user,
                receiver__email=data["receiver"]["email"],
                status=ACCEPTED,
            ).exists():
                raise serializers.ValidationError(ALREADY_FRIENDS)
            elif friend_request.filter(
                sender=request_user,
                receiver__email=data["receiver"]["email"],
                status=REJECTED,
            ).exists():
                raise serializers.ValidationError(FRIEND_REQUEST_DECLINED)
            return data
        else:
            return self.context

    def create(self, validated_data):
        sender = self.context["request"].user
        receiver = User.objects.get(email=validated_data["receiver"]["email"])
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        return friend_request

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance