import logging
from rest_framework import generics
from multiprocessing import context
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib import messages
from rest_framework.response import Response
from accounts.models import OneTimePassword
from django.contrib.auth import authenticate, login
from accounts.serializers import  (GithubLoginSerializer, GoogleSignInSerializer, InstitutionRegisterSerializer, LoginSerializer,
                                    LogoutUserSerializer, PasswordResetRequestSerializer,SetNewPasswordSerializer, 
                                    UserRegisterSerializer, VerifyUserEmailSerializer, ProfileSerializer)
from rest_framework import status
from .utils import send_generated_otp_to_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from .models import User, Profile
from django.contrib.auth import authenticate
from rest_framework.response import Response
# Create your views here.

class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user = request.data
        serializer=self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data=serializer.data
            send_generated_otp_to_email(user_data['email'], request)
            return Response({
                "status": True,
                "message": "Thanks for signing up! A passcode has been sent to verify your email.",
                "data": {
                    "user": {
                        "id": user_data['id'],  # Ensure that your serializer includes the user id.
                        'telephone': user_data['telephone'],
                        "email": user_data['email']
                    }
                }
            }, status=status.HTTP_201_CREATED)

        # Returning errors with a consistent structure.
        return Response({
            "status": False,
            "message": "Failed to register.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RegisterInstutionView(GenericAPIView):
    serializer_class = InstitutionRegisterSerializer

    def post(self, request):
        user = request.data
        serializer=self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data=serializer.data
            send_generated_otp_to_email(user_data['email'], request)
            return Response({
                "status": True,
                "message": "Thanks for signing up! A passcode has been sent to verify your email.",
                "data": {
                    "user": {
                        "id": user_data['id'],  # Ensure that your serializer includes the user id.
                        'telephone': user_data['telephone'],
                        "email": user_data['email']
                    }
                }
            }, status=status.HTTP_201_CREATED)

        # Returning errors with a consistent structure.
        return Response({
            "status": False,
            "message": "Failed to register.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class VerifyUserEmail(GenericAPIView):
    serializer_class = VerifyUserEmailSerializer

    def post(self, request):
        try:
            passcode = request.data.get('otp')
            user_pass_obj = OneTimePassword.objects.get(otp=passcode)
            user = user_pass_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'status': True,
                    'message': 'Account email verified successfully.',
                    'data': {
                        'user': {
                            "id": user.id,  # Ensure that your serializer includes the user id.
                            'full_name': user.get_full_name if hasattr(user, 'get_full_name') else f"{user.first_name} {user.last_name}",
                            "email": user.email
                        }
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': False,
                'message': 'Passcode is invalid or user is already verified.',
            }, status=status.HTTP_204_NO_CONTENT)

        except OneTimePassword.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Passcode not provided or invalid.',
            }, status=status.HTTP_400_BAD_REQUEST)
        
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        
        # Check if the serializer is valid
        if serializer.is_valid():
            # If credentials are valid, retrieve the validated data
            user_data = serializer.validated_data

            # Construct the successful login response
            response_data = {
                "status": True,
                "message": "Login successfully.",
                "data": {
                    "user": {
                        "id": user_data['id'],
                        "full_name": user_data['full_name'],
                        "email": user_data['email'],
                        "telephone": user_data['telephone'],
                        "role": user_data['role'],
                    },
                    "tokens": {
                        "access_token": user_data['access_token'],
                        "refresh_token": user_data['refresh_token'],
                    }
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # If credentials are invalid, return a custom response
            return Response({
                "status": False,
                "message": "Email or password is invalid. Please check and try again.",
                "errors": serializer.errors  # Detailed errors from serializer validation
            }, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetRequestView(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)
       
        # return Response({'message':'user with that email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    



class PasswordResetConfirm(GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':"password reset is succesful"}, status=status.HTTP_200_OK)

class ProfileDetail(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the profile associated with the user
        profile = get_object_or_404(Profile, user=user)
        serializer = self.get_serializer(profile)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')

        if not user_id:
            return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        profile = get_object_or_404(Profile, user=user)

        # Ensure the request includes both data and files (for image uploads)
        serializer = self.get_serializer(profile, data=request.data, files=request.FILES, partial=True)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LogoutApiView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
 


def adminlogin(request):
    if request.user.is_authenticated:
        # If user is already authenticated, redirect them to another page
        return redirect('dashboard') 
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            # Redirect to a success page, or wherever you want
            return redirect('dashboard')
        else:
            # Display an error message if authentication fails
            messages.error(request, 'Invalid email or password.')
            return redirect('adminlogin')

    return render(request, "admin/auth/login.html")


# class GoogleOauthSignInview(GenericAPIView):
#     serializer_class=GoogleSignInSerializer

#     def post(self, request):
#         print(request.data)
#         serializer=self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data=((serializer.validated_data)['access_token'])
#         return Response(data, status=status.HTTP_200_OK) 
        


# class GithubOauthSignInView(GenericAPIView):
#     serializer_class=GithubLoginSerializer

#     def post(self, request):
#         serializer=self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             data=((serializer.validated_data)['code'])
#             return Response(data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)