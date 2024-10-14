from django.contrib import admin
from django.urls import path
from .views import ProjectListCreateViews, ProjectListUpdateDeleteView

app_name = 'projects'

urlpatterns = [
    path('list/create/', ProjectListCreateViews.as_view(), name='project_list_create'),
    path('update/destroy/<int:pk>/', ProjectListUpdateDeleteView.as_view(), name='project_list_update_delete'),
]
