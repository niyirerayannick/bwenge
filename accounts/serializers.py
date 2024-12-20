
from accounts.managers import UserManager
from bwenge import settings
from core.models import Institution
from .models import User, Profile
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .google import Google, register_social_user
from .github import Github

class InstitutionRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'telephone', 'first_name', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate_telephone(self, value):
        if User.objects.filter(telephone=value).exists():
            raise serializers.ValidationError("A user with that telephone already exists.")
        return value

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        institution = User.objects.create_institution(
            email=validated_data['email'],
            telephone=validated_data.get('telephone'),
            name=validated_data.get('first_name'),  # assuming name is stored in first_name
            password=validated_data.get('password')
        )
        return institution


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2= serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields = ['id','email','telephone', 'first_name', 'last_name', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate_telephone(self, value):
        if User.objects.filter(telephone=value).exists():
            raise serializers.ValidationError("A user with that telephone already exists.")
        return value

    def validate(self, attrs):
        password=attrs.get('password', '')
        password2 =attrs.get('password2', '')
        if password !=password2:
            raise serializers.ValidationError("passwords do not match")
         
        return attrs

    def create(self, validated_data):
        user= User.objects.create_user(
            email=validated_data['email'],
            telephone=validated_data.get('telephone'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
            )
        return user
    
class VerifyUserEmailSerializer(serializers.Serializer):
    otp = serializers.CharField()
    role = serializers.CharField(max_length=50, read_only=True)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    telephone = serializers.CharField(max_length=15, read_only=True)  # Added telephone field
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = User
        fields = ['id','email', 'password', 'full_name', 'access_token', 'refresh_token','role']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        user = authenticate(request, username=email, password=password)

        if not user:
            raise AuthenticationFailed("Email or password is invalid. Please check and try again.")

        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified.")

        refresh = RefreshToken.for_user(user)
        
        user_data = {
            'id': user.id,
            'email': user.email,
            'full_name': user.get_full_name if hasattr(user, 'get_full_name') else f"{user.first_name} {user.last_name}",
            'telephone': user.telephone,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'role': user.role,
        }

        return user_data

    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user= User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            base_url = "https://www.bwenge.com"
            relative_link =reverse('reset-password-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abslink = f"{base_url}{relative_link}"
            email_body = f"Hi {user.first_name},\n\nUse the link below to reset your password:\n{abslink}\n\nIf you did not request a password reset, please ignore this email."
            data={
                'email_body':email_body, 
                'email_subject':"Reset your Password", 
                'to_email':user.email
                }
            send_normal_email(data)

        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)
    token=serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("reset link is invalid or has expired", 401)
            if password != confirm_password:
                raise AuthenticationFailed("passwords do not match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("link is invalid or has expired")
        
class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')

        return attrs

    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        
class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_picture']

    def validate_profile_picture(self, value):
        """
        Optionally validate the profile picture. 
        Here, you can add custom validation if necessary (e.g., file size or file type).
        """
        if value:
            if value.size > 5 * 1024 * 1024:  # 5 MB max size
                raise serializers.ValidationError("Profile picture is too large. Maximum size allowed is 5MB.")
        return value


class GoogleSignInSerializer(serializers.Serializer):
    access_token=serializers.CharField(min_length=6)


    def validate_access_token(self, access_token):
        user_data=Google.validate(access_token)
        try:
            user_data['sub']
            
        except:
            raise serializers.ValidationError("this token has expired or invalid please try again")
        
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
                raise AuthenticationFailed('Could not verify user.')

        user_id=user_data['sub']
        email=user_data['email']
        first_name=user_data['given_name']
        last_name=user_data['family_name']
        provider='google'

        return register_social_user(provider, email, first_name, last_name)


class GithubLoginSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, code):   
        access_token = Github.exchange_code_for_token(code)

        if access_token:
            user_data=Github.get_github_user(access_token)

            full_name=user_data['name']
            email=user_data['email']
            names=full_name.split(" ")
            firstName=names[1]
            lastName=names[0]
            provider='github'
            return register_social_user(provider, email, firstName, lastName)

        