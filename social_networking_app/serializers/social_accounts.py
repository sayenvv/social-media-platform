from datetime import datetime
from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import serializers

from social_networking_app.constants.constant_variables import ACCEPTED
from social_networking_app.constants.constant_variables import (
    MAX_FRIEND_REQUESTS_PER_MINUTE,
)
from social_networking_app.constants.constant_variables import PENDING
from social_networking_app.constants.constant_variables import REJECTED
from social_networking_app.constants.constant_variables import TIME_DELTA_VARIABLE
from social_networking_app.constants.messages import ACCOUNT_NOT_FOUND
from social_networking_app.constants.messages import ALREADY_FRIENDS
from social_networking_app.constants.messages import FRIEND_REQUEST_DECLINED
from social_networking_app.constants.messages import FRIEND_REQUEST_LIMIT_EXCEEDED
from social_networking_app.constants.messages import INVALID_FRIEND_REQUEST
from social_networking_app.constants.messages import REQUEST_ALREADY_SENT
from social_networking_app.models import FriendRequest
from social_networking_app.models import User


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "phone_number")


class FriendRequestSerializer(serializers.ModelSerializer):
    receiver_username = serializers.CharField(
        source="receiver.email"
    )  # Show receiver username
    # sender = serializers.CharField(source="sender.email")  # Show sender username

    class Meta:
        model = FriendRequest
        fields = ("id", "sender", "receiver_username", "status", "created_at")
        read_only_fields = (
            "sender",
            "status",
            "created_at",
        )  # Sender and status are set automatically

    def validate(self, attrs):
        friend_request = FriendRequest.objects
        request_user = self.context["request"].user
        if not self.context.get("id"):

            # Check if user is trying to send a request to themselves
            if request_user.email == attrs["receiver"]["email"]:
                raise serializers.ValidationError(INVALID_FRIEND_REQUEST)
            one_minute_ago = datetime.now() - timedelta(minutes=TIME_DELTA_VARIABLE)

            friend_request_count = friend_request.filter(
                sender=request_user,
                created_at__gte=one_minute_ago,
                created_at__lte=datetime.now(),
            ).aggregate(count=Count("*"))["count"]
            if friend_request_count > MAX_FRIEND_REQUESTS_PER_MINUTE:
                raise serializers.ValidationError(FRIEND_REQUEST_LIMIT_EXCEEDED)
            # Check if a pending request already exists
            if friend_request.filter(
                sender=request_user,
                receiver__email=attrs["receiver"]["email"],
                status=PENDING,
            ).exists():
                raise serializers.ValidationError(REQUEST_ALREADY_SENT)
            elif friend_request.filter(
                sender=request_user,
                receiver__email=attrs["receiver"]["email"],
                status=ACCEPTED,
            ).exists():

                raise serializers.ValidationError(ALREADY_FRIENDS)
            elif friend_request.filter(
                sender=request_user,
                receiver__email=attrs["receiver"]["email"],
                status=REJECTED,
            ).exists():
                raise serializers.ValidationError(FRIEND_REQUEST_DECLINED)
            return attrs
        else:
            if friend_request.filter(
                id=self.context["id"],
                status=ACCEPTED,
            ).exists():
                raise serializers.ValidationError(ALREADY_FRIENDS)
            return self.context

    def create(self, validated_data):
        sender = self.context["request"].user
        try:
            receiver = User.objects.get(email=validated_data["receiver"]["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(ACCOUNT_NOT_FOUND)
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        return friend_request

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
