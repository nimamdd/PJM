from django.urls import path
from .views import (ProfileCreate, ProfileDetail, ChangePasswordProfile, PasswordResetRequestView,
                    PasswordResetConfirmView, UserLoginView, UserLogoutView,
                    TeamCreate, TeamDetailUpdateDestroy)

app_name = 'accounts'

urlpatterns = [
    path('create/profile/', ProfileCreate.as_view(), name='create_profile'),
    path('profile/<int:id>/', ProfileDetail.as_view(), name='profile_detail'),
    path('change/password/', ChangePasswordProfile.as_view(), name='profile_change_password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='profile_logout'),
    path('create/team/', TeamCreate.as_view(), name='create_team'),
    path('team/detail/update/destroy/<int:id>/', TeamDetailUpdateDestroy.as_view(), name='team_detail_update_delete')
]
