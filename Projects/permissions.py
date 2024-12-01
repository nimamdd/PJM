from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from .models import Project, Task, SubTask
from django.shortcuts import get_object_or_404


class CanAssignAdmins(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        project_id = view.kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id)

        team = project.team.first()
        if not team:
            raise ValidationError("This project does not have an associated team")

        team_admins = team.admin.all()
        admins = request.data.get('admins', [])

        for admin_id in admins:
            admin_user = get_object_or_404(User, id=admin_id)

            if not admin_user.is_premium:
                raise ValidationError(f"User with ID {admin_id} is not a premium user")

            if not team_admins.filter(id=admin_id).exists():
                raise ValidationError(f"User with ID {admin_id} is not an admin of the project's team")

        return True


class CanAssignMembers(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method != 'POST':
            return True

        project_id = view.kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id)
        task_id = view.kwargs.get('task_pk')
        task = get_object_or_404(Task, id=task_id)

        team = project.team.first()
        if not team:
            raise ValidationError("This project does not have an associated team")

        team_members = team.members.all()
        members = request.data.get('members', [])

        for member_id in members:
            member_user = get_object_or_404(User, id=member_id)

            if not member_user.is_premium:
                raise ValidationError(f"User with ID {member_id} is not a premium user")

            if not team_members.filter(id=member_id).exists():
                raise ValidationError(f"User with ID {member_id} is not a member of the project's team")

        return True







class CanCreateProject(permissions.BasePermission):
    """
    Custom permission to check if user can create Project
    """

    def has_permission(self, request, view):
        user = request.user
        if request.method != 'POST':
            return True

        if not user.is_premium and user.task_counter > 5:
            return False
        return True


class CanViewProject(permissions.BasePermission):
    """
    Custom permission to check if the user has permission to view a specific project.
    """

    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get('pk')

        # Premium permission (if it be needed to check premium condition)
        if not user.is_premium and user.project_counter >= 5:
            raise ValidationError('You must be a premium user to access more than 5 projects.')

        # Ownership or Team Membership
        if project_id:
            project = get_object_or_404(Project, id=project_id)

            # Check if the user is the owner of the project
            if project.owner == user:
                return True

            # Check if the user is an admin of the project's team
            team = project.team.first()
            if team and user in team.admin.all():
                return True

            # Check if the user is a member of the project's team
            if team and user in team.members.all():
                return True

            # If the user is not owner, admin, or member of the team, deny access
            return False

        return True


class CanUpdateDestroyProject(permissions.BasePermission):
    """
    custom permission to check if the user can update or delete project
    """

    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id)

        try:
            if user == project.owner:
                return True
        except user.DoesNotExist or project.DoesNotExist:
            pass
        return False


class CanCreateTask(permissions.BasePermission):
    """
    Custom permission to check if the user has permission to create tasks of a specific project
    """
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        project_id = view.kwargs.get('pk')
        project = get_object_or_404(Project, id=project_id)
        user = request.user
        team = project.team.first()

        if not project_id:
            return False

        if user.is_premium:
            if team and (user in team.admin.all() or user == project.owner):
                return True
            else:
                return False
        else:
            if user.project_counter > 5:
                return False
            else:
                return True


class CanViewTask(permissions.BasePermission):
    """
    Custom permission to check if the user has permission to view tasks of a specific project.
    """

    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs.get('pk')

        # Premium permission
        if not user.is_premium and user.task_counter >= 5:
            raise ValidationError('You must be a premium user to create more than 5 tasks.')

        # Ownership or Team Membership
        if project_id:
            project = get_object_or_404(Project, id=project_id)

            # Check if the user is the owner of the project
            if project.owner == user:
                return True

            # Check if the user is an admin of the project's team
            team = project.team.first()
            if team and user in team.admin.all():
                return True

            # Check if the user is a member of the project's team
            if team and user in team.members.all():
                return True

            # If the user is not owner, admin, or member of the team, deny access
            return False

        return True


class CanUpdateDestroyTask(permissions.BasePermission):
    """
    Custom permission to check if the user can Update or Destroy a Task.
    """

    def has_permission(self, request, view):
        user = request.user
        task_id = view.kwargs.get('pk')
        task = get_object_or_404(Task, id=Task)
        if task:
            project = Project.objects.get(id=task.project.id)

        try:

            if user == project.user:
                return True
        except user.DoesNotExist or project.DoseNotExist:
            pass

        return False


class CanCreateSubtask(permissions.BasePermission):
    """
    Custom permission to check if the user has permission to create subtasks of a specific task
    """
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True

        task_id = view.kwargs.get('pk')
        if not task_id:
            return False

        task = get_object_or_404(Task, id=task_id)
        project = task.project
        user = request.user
        team = project.team.first()

        if user.is_premium:
            if team and (user in team.members.all() or user == project.owner):
                return True
            return False

        if user.task_counter > 5:
            return False

        if team and (user in team.admin.all() or user == project.owner):
            return True

        return False


class CanViewSubtask(permissions.BasePermission):
    """
    Custom permission to check if the user has permission to view a specific subtask.
    """

    def has_permission(self, request, view):
        user = request.user
        subtask_id = view.kwargs.get('pk')

        # Premium permission (if it be needed to check permission condition)
        if not user.is_premium and user.subtask_counter >= 5:
            raise ValidationError('You must be a premium user to access more than 5 subtasks.')

        # Ownership or Team Membership for the task
        if subtask_id:
            subtask = get_object_or_404(SubTask, id=subtask_id)
            task = subtask.task
            project = task.project

            # Check if the user is the owner of the project
            if project.owner == user:
                return True

            # Check if the user is an admin of the project's team
            team = project.team.first()
            if team and user in team.admin.all():
                return True

            # Check if the user is a member of the project's team
            if team and user in team.members.all():
                return True

            # If the user is not owner, admin, or member of the team, deny access
            return False

        return True


class CanUpdateDestroySubtask(permissions.BasePermission):
    """
    Custom permission to check if the user can Update or Destroy
    """
    def has_permission(self, request, view):
        user = request.user
        subtask_id = view.kwargs.get('pk')
        subtask = get_object_or_404(SubTask, id=subtask_id)

        if subtask:
            project = Project.objects.get(id=subtask.project.id )

        try:
            if user == project.owner :
                return True
        except user.DoesNotExist or Project.DoesNotExist:
            return False
