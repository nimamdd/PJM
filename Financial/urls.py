from django.urls import path
from .views import FinancialListCreateView

app_name = 'financial'

urlpatterns = [
    path('list/create/', FinancialListCreateView.as_view(), name='list_create_financial_record')
]
