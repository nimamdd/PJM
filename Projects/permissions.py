from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Project
from django.shortcuts import get_object_or_404


class CanUpdateDestroyProject(permissions.BasePermission):
    """
    custom permision to check if the user can update or delete project
    """

    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id)

        try:
            if user == project.user:
                return True
        except user.DoesNotExist or project.DoesNotExist:
            pass
        return False
