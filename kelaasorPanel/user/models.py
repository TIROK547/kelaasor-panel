from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

def validate_not_only_letters(value):
    if value.isalpha():
        raise ValidationError("رمز عبور نباید فقط شامل حروف باشد. لطفاً از اعداد یا نمادها هم استفاده کنید.")
    
def validate_phone_number(value):
    try:
        phone = phonenumbers.parse(value, "IR")
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("شماره وارد شده معتبر نیست.")
    except phonenumbers.NumberParseException:
        raise ValidationError("فرمت شماره وارد شده نادرست است.")


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, user_name, password=None):
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
    
    def create_superuser(self, phone_number:str, user_name:str = "admin", password:str = "admin123"):
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
        validators=[validate_phone_number]
    )
    date_created = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100, blank=True, null=True, validators=[MinLengthValidator(8), validate_not_only_letters])
    national_id = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=["phone_number"])
        ]

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['password']
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.phone_number
