from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core import models
from django.db import models
from core.models import Institution
from .managers import  UserManger
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import Permission

class UserRolePermissions:
    @staticmethod
    def assign_permissions(user):
        if user.role == 'user':
            # Define permissions for regular users here
            pass
        elif user.role == 'institution_admin':
            # Define permissions for institution admins here
            user.user_permissions.set(Permission.objects.all())
            # user.user_permissions.add(Permission.objects.get(codename='add_student'))
            # user.user_permissions.add(Permission.objects.get(codename='change_student'))
            # user.user_permissions.add(Permission.objects.get(codename='delete_student'))
        elif user.role == 'system_admin':
            # Define permissions for system admins here
            user.user_permissions.set(Permission.objects.all())


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email Address")
    # telephone = models.CharField(max_length=15, unique=True, verbose_name=_("Telephone"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    USER_ROLE_CHOICES = [
        ('user', 'User'),
        ('institution_admin', 'Institution Admin'),
        ('system_admin', 'System Admin'),
    ]
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES, default='user')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManger()
    
    def __str__(self):
        return self.first_name
    
    @property
    def get_full_name(self): 
        return f"{self.first_name} {self.last_name}"
    
    def tokens(self):
        pass

class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.first_name} - otp code"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.email


