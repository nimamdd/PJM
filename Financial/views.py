from .models import FinancialRecord
from .serializers import FinancialRecordSerializers
from rest_framework import generics
from .filters import ListOfFinancialPerformanceFilterBackend


class FinancialListCreateView(generics.ListCreateAPIView):
    """

    """
    serializer_class = FinancialRecordSerializers
    filter_backends = [ListOfFinancialPerformanceFilterBackend]

    def get_queryset(self):
        user = self.request.user
        return FinancialRecord.objects.filter(who_created=user).order_by('-price')

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(who_created=self.request.user)
