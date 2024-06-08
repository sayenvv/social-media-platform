"""models class for the app"""
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
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


class User(AbstractBaseUser, PermissionsMixin):
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
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        """Meta class"""

        verbose_name = "user"
        verbose_name_plural = "users"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Signal handler that automatically creates an authentication token for a new user.

    This function is triggered whenever a user is saved using the `post_save` signal
    of the custom user model specified in `settings.AUTH_USER_MODEL`. It checks the
    `created` flag to ensure a token is only created for newly created users.

    Args:
        sender (class): The sender of the signal (usually the User model).
        instance (User, optional): The instance of the User model that was saved. Defaults to None.
        created (bool): A flag indicating if the user was created or updated. Defaults to False.
        **kwargs (dict): Additional keyword arguments passed to the signal handler.

    Returns:
        dict (optional): A dictionary containing the key of the newly created token (if a token was created).
    """

    if created:
        token = Token.objects.create(user=instance)
        return {"token": token.key}

    # No token creation for existing users or updates
    return None


class FriendRequest(models.Model):
    """
    Represents a friend request between two users.
    """

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requests_sent",
        help_text="The user who sent the friend request.",
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requests_received",
        help_text="The user who is receiving the friend request.",
    )

    status = models.CharField(
        max_length=20,
        choices=(
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ),
        default="pending",
        help_text="The current status of the friend request.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    """
    The date and time the friend request was created. This field is automatically
    populated when the friend request is saved.
    """

    class Meta:
        """Meta class"""

        unique_together = (("sender", "receiver"),)  # Prevent duplicate requests

    def __str__(self):
        return f"{self.sender.name} -> {self.receiver.name} ({self.status})"
