import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def generate_unique_code():
    """
    generate unique code for user
    """
    model = User
    while True:
        code = str(uuid.uuid4()).replace("-", "").upper()[:6]
        try:
            if not model.objects.filter(pk=code).exists():
                break
        except Exception as e:
            return code
    return code


class CustomUserManager(BaseUserManager):

    def create_user(self, email, full_name, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, full_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, full_name, password, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    """
    this is a custom user model with mobile number
    """
    id = models.CharField(max_length=255, primary_key=True,
                          default=generate_unique_code)
    full_name = models.CharField(_("full name"), max_length=255, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.full_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.full_name.strip().split(" ")[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        with mail.get_connection() as connection:
            mail.EmailMessage(
                subject, message, from_email, [
                    self.email], connection=connection, **kwargs).send()
        # send_mail(subject, message, from_email, [self.email], **kwargs)


class User(BaseUser):
    """
    this is a custom user model extending BaseUser
    """

    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    institiution = models.CharField(max_length=50, blank=False, null=False, default="College/Institiution")
