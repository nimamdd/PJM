from .models import Project
from rest_framework import generics
from .permissions import permissions, CanUpdateDestroyProject
from .serializers import ProjectSerializers


class ProjectListCreateViews(generics.ListCreateAPIView):
    serializer_class = ProjectSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)


class ProjectListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializers
    permission_classes = [permissions.IsAuthenticated, CanUpdateDestroyProject]
    queryset = Project
    lookup_field = 'pk'

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


