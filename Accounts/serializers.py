from rest_framework import serializers
from .models import Profile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'username',
            'email',
            'image',
            'project_counter',
            'project_percentage_done',
            'task_counter',
            'task_percentage_done',
            'subtask_counter',
            'subtask_percentage_done',
            'count_all_financial_record',
            'how_many_paid',
            'how_many_in_progress',
            'how_many_canceled',
        ]

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile


class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "new password fields didn't match"})
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password], required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "new password fields didn't match"})
        return attrs

    def save(self, profile):
        profile.set_password(self.validated_data['new_password'])
        profile.save()
        return profile


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except Exception as e:
            raise ValidationError("Invalid token or token already blacklisted")
