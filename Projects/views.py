from .models import Project, Task, SubTask
from rest_framework import generics
from .permissions import permissions, CanUpdateDestroyProject, CanUpdateDestroyTask, CanUpdateDestroySubtask
from .serializers import ProjectSerializers, TaskSerializer, SubtaskSerializers
from django.shortcuts import get_object_or_404
from .paginations import ProjectTaskSubtaskPagination
from rest_framework.exceptions import PermissionDenied, ValidationError



class ProjectListCreateViews(generics.ListCreateAPIView):
    serializer_class = ProjectSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProjectTaskSubtaskPagination

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_premium and self.request.user.total_cases > 5:
            raise ValidationError('You must be premium user for creating more than 5 Project')
        if serializer.is_valid():
            serializer.save(owner=self.request.user)


class ProjectListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializers
    permission_classes = [permissions.IsAuthenticated, CanUpdateDestroyProject]
    #queryset = Project
    lookup_field = 'pk'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class TaskProjectListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProjectTaskSubtaskPagination


    def get_queryset(self):
        project_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=project_id)

        if project.owner != self.request.user:
            raise PermissionDenied("You don't have permission to view tasks of this project")
        return Task.objects.filter(project=project)

    def perform_create(self, serializer):
        project_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=project_id)

        if not self.request.user.is_premium and self.request.user.task_counter > 5:
            raise ValidationError('You must be premium user for creating more than 5 Tasks')

        if project.owner != self.request.user:
            raise PermissionDenied("Only the owner can add tasks to this project")
        serializer.save(project=project)

        # get admins and teams of project
        team = project.team.first()  # if only one team
        if not team:
            raise ValidationError("This project does not have an associated team")

        team_admins = team.admin.all()

        # get admins from validated date
        admins = serializer.validated_data.get('admins', [])

        # check if all task admins are team admins
        for admin in admins:
            if admin not in team_admins:
                raise ValidationError(f'{admin} is not an admin of the project\'s team')
        serializer.save(project=project)


class TaskListUpdateDeleteViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, CanUpdateDestroyTask]
    #queryset = Task
    lookup_field = 'pk'

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def perform_update(self, serializer):
        task=self.get_object()
        if not serializer.validated_data.get('image',None):
            serializer.validated_data['iamge']=task.image
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class SubtaskListCreate(generics.ListCreateAPIView):
    serializer_class = SubtaskSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProjectTaskSubtaskPagination
    # lookup_field = 'pk'

    def get_queryset(self):
        task_id = self.kwargs['pk']
        task = get_object_or_404(Task, id=task_id)
        if not self.request.user.is_premium and self.request.user.subtask_counter > 5:
            raise ValidationError('You must be premium user for creating more than 5 Subtasks')

        if task.project.owner != self.request.user:
            raise PermissionDenied("You don't have permission to view subtasks of this task.")
        return SubTask.objects.filter(task=task)

    def perform_create(self, serializer):
        task_id = self.kwargs['pk']
        task = get_object_or_404(Task, id=task_id)

        if task.project.owner != self.request.user:
            raise PermissionDenied("Only the owner can add subtasks to this task.")

        serializer.save(task=task)


class SubtaskListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubtaskSerializers
    permission_classes = [permissions.IsAuthenticated , CanUpdateDestroySubtask]
    lookup_field = 'pk'

    def get_queryset(self):
        return SubTask.objects.filter(project__owner=self.request.user,)
    def perform_update(self, serializer):
        subtask = self.get_object()
        if not serializer.validated_data.get('image',None):
            serializer.validated_data['image']= subtask.image
        serializer.save()

    def perform_delete(self, instance):
        instance.delete()


