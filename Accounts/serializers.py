from rest_framework import serializers
from .models import Profile, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        if "password" in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ProfileSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Profile
        fields = [
            'pk',
            'user',
            'image',
            'phone',
        ]

    def create(self, validated_data):
        # Extract the nested user data
        user_data = validated_data.pop('user')

        # Create the user
        user = UserSerializers.create(UserSerializers(), validated_data=user_data)

        # Create the profile linked to the created user
        profile = Profile.objects.create(user=user, **validated_data)

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
