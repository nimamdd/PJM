from django.urls import path
from .views import (ProfileCreate, ProfileDetail, ChangePasswordProfile, PasswordResetRequestView,
                    PasswordResetRequestView, UserLogoutView)

app_name = 'accounts'

urlpatterns = [
    path('create/profile/', ProfileCreate.as_view(), name='create_profile'),
    path('profile/', ProfileDetail.as_view(), name='profile_detail'),
    path('change/password/', ChangePasswordProfile.as_view(), name='profile_change_password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetRequestView.as_view(), name='password_reset_confirm'),
    path('logout/', UserLogoutView.as_view(), name='profile_logout'),
]
