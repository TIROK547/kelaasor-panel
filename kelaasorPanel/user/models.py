from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

# Validator to ensure password is not letters only (must include numbers or symbols)
def validate_not_only_letters(value):
    if value.isalpha():
        raise ValidationError("Password must not contain only letters. Please include numbers or symbols.")

# Validator to check if phone number is a valid Iranian phone number
def validate_phone_number(value):
    try:
        phone = phonenumbers.parse(value, "IR")
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("The phone number entered is not valid.")
    except phonenumbers.NumberParseException:
        raise ValidationError("Invalid phone number format.")


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, user_name, password=None):
        # Create a regular user with validated phone number
        if not phone_number:
            raise ValueError("User must have a phone number")

        try:
            phone = phonenumbers.parse(phone_number, "IR")
            if not phonenumbers.is_valid_number(phone):
                raise ValueError("Invalid phone number")
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format")

        user = self.model(
            phone_number=phone_number,
            user_name=user_name
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone_number: str, user_name: str = "admin", password: str = "admin123"):
        # Create a superuser with full permissions
        user = self.create_user(
            phone_number=phone_number,
            user_name=user_name,
            password=password,
            email=None
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    email = models.EmailField(max_length=120, unique=True, blank=True, null=True)
    user_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[validate_phone_number]  # Phone number validation
    )
    date_created = models.DateTimeField(auto_now_add=True)
    password = models.CharField(
        max_length=100, blank=True, null=True,
        validators=[MinLengthValidator(8), validate_not_only_letters]  # Min length 8 and must include number/symbol
    )
    national_id = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Designates user as staff (can access admin)
    is_superuser = models.BooleanField(default=False)  # Designates user as superuser
    
    class Meta:
        indexes = [
            models.Index(fields=["phone_number"])  # Index on phone_number for faster lookups
        ]

    USERNAME_FIELD = 'phone_number'  # Use phone number as the unique identifier
    REQUIRED_FIELDS = ['password']    # Required fields when creating user
    objects = UserManager()           # Custom user manager

    def has_perm(self, perm, obj=None):
        # Only superusers have permissions
        return self.is_superuser

    def has_module_perms(self, app_label):
        # Only superusers have module permissions
        return self.is_superuser

    def __str__(self):
        # String representation of the user is their phone number
        return self.phone_number
