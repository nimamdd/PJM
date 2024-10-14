from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .serializers import UserSerializers, ProfileSerializers, ChangePasswordSerializers
from .models import Profile, User


class UserCreate(generics.CreateAPIView):
    """
    This view creates a user and profile together using nested serializers.
    """
    serializer_class = ProfileSerializers

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class UserProfileDetail(generics.ListAPIView):
    """
     get user profile
    """
    serializer_class = ProfileSerializers
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class ChangePasswordUser(generics.UpdateAPIView):
    """
    change user pass
    """
    serializer_class = ChangePasswordSerializers
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                response = {
                    'status': 'Error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': "something went wrong",
                    'data': []
                }
                return Response(response)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()

            response = {
                'status': 'sucess',
                'code': status.HTTP_200_OK,
                'message': "password updated successfully",
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
