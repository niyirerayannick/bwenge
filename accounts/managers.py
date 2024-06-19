from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.models import Institution

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        self.email_validator(email)
        if not first_name:
            raise ValueError(_("The First Name field must be set"))

        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, first_name, last_name, password, **extra_fields)

    def create_institution(self, email, telephone, name, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'institution_admin')

        if not email:
            raise ValueError(_("The Email field must be set"))
        if not telephone:
            raise ValueError(_("The Telephone field must be set"))
        if not name:
            raise ValueError(_("The Name field must be set"))

        email = self.normalize_email(email)
        self.email_validator(email)

        institution_admin = self.create_user(
            email=email,
            first_name=name,
            last_name='',  # Set to an empty string or any default value
            password=password,
            telephone=telephone,
            **extra_fields
        )
        institution_admin.role = 'institution_admin'
        institution_admin.save(using=self._db)
        return institution_admin
