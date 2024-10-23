from rest_framework import permissions
from django.contrib.auth.models import User
from .models import FinancialRecord
from django.shortcuts import get_object_or_404


class CanUserSelectThisFinancialRecord(permissions.BasePermission):
    """
    custom perm to check this user can update or destroy
    """

    def has_permission(self, request, view):
        user = request.user
        record_id = view.kwargs.get('pk')
        record = get_object_or_404(FinancialRecord, id=record_id)
        try:
            if user == record.who_created:
                return True
        except user.DoesNotExist or record.DoesNotExist:
            return False
        return False
