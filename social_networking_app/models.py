from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """
    Custom user manager to support email as username and create superuser with email.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, password and extra fields.
        """
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        print("herere")
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, password and extra fields.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if password is None:
            raise ValueError("Superuser must have a password")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Custom User model with email as username, name, and phone number.
    """

    email = models.EmailField(unique=True, verbose_name="email address")
    name = models.CharField(max_length=255, verbose_name="full name")
    phone_number = models.CharField(
        max_length=20, blank=True, verbose_name="phone number"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False
    )  # a user who can access the admin site
    is_superuser = models.BooleanField(
        default=False
    )  # a superuser who has all permissions

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        print(token.key)
        return {"token": token.key}


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests_sent"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests_received"
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ),
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("sender", "receiver"),)  # Prevent duplicate requests

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name} ({self.status})"
