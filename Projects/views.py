from .models import Project, Task, SubTask
from rest_framework import generics
from .permissions import (CanAssignAdmins, CanAssignMembers, CanCreateProject, CanViewProject,
                          CanUpdateDestroyProject, CanCreateTask, CanViewTask, CanUpdateDestroyTask,
                          CanCreateSubtask, CanViewSubtask, CanUpdateDestroySubtask)
from .serializers import ProjectSerializers, TaskSerializer, SubtaskSerializers
from .paginations import ProjectTaskSubtaskPagination
from django.shortcuts import get_object_or_404


class ProjectListCreateViews(generics.ListCreateAPIView):
    serializer_class = ProjectSerializers
    permission_classes = [CanCreateProject]
    pagination_class = ProjectTaskSubtaskPagination

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializers
    permission_classes = [CanUpdateDestroyProject]
    lookup_field = 'pk'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class TaskProjectListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [CanViewTask, CanCreateTask, CanAssignAdmins]
    pagination_class = ProjectTaskSubtaskPagination

    def get_queryset(self):
        project_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=project_id)
        return Task.objects.filter(project=project)

    def perform_create(self, serializer):
        project_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=project_id)
        task = serializer.save(project=project)
        task.admins.add(project.owner)


class TaskListUpdateDeleteViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [CanUpdateDestroyTask]
    lookup_field = 'pk'

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)


class SubtaskListCreate(generics.ListCreateAPIView):
    serializer_class = SubtaskSerializers
    permission_classes = [CanViewSubtask, CanCreateSubtask]
    pagination_class = ProjectTaskSubtaskPagination

    def get_queryset(self):
        task_id = self.kwargs['pk']
        task = get_object_or_404(Task, id=task_id)
        return SubTask.objects.filter(task=task)

    def perform_create(self, serializer):
        task_id = self.kwargs['pk']
        task = get_object_or_404(Task, id=task_id)
        subtask = serializer.save(task=task)
        subtask.members.add(task.project.owner)


class SubtaskListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubtaskSerializers
    permission_classes = [CanUpdateDestroySubtask]
    lookup_field = 'pk'

    def get_queryset(self):
        return SubTask.objects.filter(task__project__owner=self.request.user)
