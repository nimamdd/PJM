from django.contrib import admin
from .models import Project, Task, SubTask
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'color', 'status', 'image_thumbnail',)
    list_filter = ('color', 'status',)
    list_editable = ('color', 'status',)
    #search_fields = ('user__username', 'user__last_name', 'user__first_name', 'user__email',)
    list_per_page = 10
    fields = (
        ('title','image_thumbnail','image'),
        ('owner', 'team'),
        ('description', 'status','color'),
        ('start_date','end_date'),
        ('budget'),

    )


@admin_thumbnails.thumbnail('image')
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','project', 'color', 'status', 'image_thumbnail',)
    list_filter = ('color', 'status',)
    list_editable = ('color', 'status',)
    #search_fields = ('project__user__username',)
    list_per_page = 10
    fields = (
        ('title', 'status', ),
        'description',
        ('project', 'admins',),
        'budget'
    )


@admin_thumbnails.thumbnail('image')
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'color', 'status', 'image_thumbnail',)
    list_filter = ('color', 'status',)
    list_editable = ('color', 'status',)
    #search_fields = ('task__project__user__username',)
    list_per_page = 10
    fields = (
        ('title','image_thumbnail','image'),
        ('members', ),
        ('description', 'status', 'color'),
        ('start_date', 'end_date'),
        'budget',
            )



admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
