from audioop import reverse

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from jwt.utils import force_bytes
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (ProfileSerializers, ChangePasswordSerializers,
                          PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
                          LoginSerializer,UserLogoutSerializer,
                          TeamSerializer)
from .models import Profile, Team


class ProfileCreate(generics.CreateAPIView):
    """
    This view is used to create Profile
    """
    serializer_class = ProfileSerializers
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save()


class ProfileDetail(generics.RetrieveAPIView):
    """
    Get profile Details
    """
    serializer_class = ProfileSerializers
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        return Profile.objects.all()


class ChangePasswordProfile(generics.UpdateAPIView):
    """
    change profile password
    """
    serializer_class = ChangePasswordSerializers
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not profile.check_password(serializer.data.get('old_password')):
                response = {
                    'status': 'Error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': "something went wrong",
                    'data': []
                }
                return Response(response)

            profile.set_password(serializer.data.get('new_password'))
            profile.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': "password updated successfully",
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    """
    request for password reset
    """
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        profile = Profile.objects.filter(email=email).first()
        if profile:
            token = default_token_generator.make_token(profile)
            uid = urlsafe_base64_encode(force_bytes(profile.pk))
            reset_url = request.build_absolute_uri(
                reverse('accounts:password-rest-confirm', kwargs={'uidb64': uid, 'token': token})
            )
            send_mail('Password Reset Request',
                      f'Click the link below to reset your password: {reset_url}',
                      'from@example.com',
                      [email],
                      fail_silently=False, )
        return Response({'detail': 'Password reset link has been sent'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    confirm the password reset
    """
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            profile = Profile.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
            profile = None
        if profile and default_token_generator.check_token(profile, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(profile)
            return Response({"detail": 'Password has been reset successfully'})
        else:
            return Response({"detail": 'Invalid token or expired link'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):
    """
    Login user
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(views.APIView):
    """
    logout user
    """
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Logout successful", status=status.HTTP_200_OK)


class TeamCreate(generics.CreateAPIView):
    """
    This view is used to create Teaam
    """
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'id'
    def get_queryset(self):
        return Team.objects.all()

    
class TeamDetail(generics.RetrieveAPIView):
    """
    Retrieve the details of a specific team.
    """
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Team.objects.all()


class TeamlUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        return Team.objects.all()