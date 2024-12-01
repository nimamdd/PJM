from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from Accounts.models import VerificationCode


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        authenticated_user = super().authenticate(request)
        if authenticated_user:
            user = authenticated_user[0]
            if VerificationCode.objects.filter(user=user).exists():
                raise PermissionDenied("Two-factor authentication is required.")
        return authenticated_user
