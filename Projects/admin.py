from django.contrib import admin
from .models import Project, Task, SubTask
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'color', 'status', 'image_thumbnail',)
    list_filter = ('color', 'status', )
    list_editable = ('color', 'status',)
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
    list_filter = ('color', 'status',)#'team')
    list_editable = ('color', 'status',)
    #search_fields = ('project__user__username',)
    list_per_page = 10
    fields = (
        ('title', 'status', ),
        ('project',),
        ('display_team', 'admins'),
        'description',
        'budget'
    )
    readonly_fields = ('display_team',)

    def display_team(self, obj):
        if obj.project:
            return ", ".join([team.name for team in obj.project.team.all()])
    display_team.short_description = 'Project Team'


@admin_thumbnails.thumbnail('image')
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'color', 'status', 'image_thumbnail',)
    list_filter = ('color', 'status',)#'team')
    list_editable = ('color', 'status',)
    list_per_page = 10
    fields = (
        ('title', 'image_thumbnail', 'image'),
        ('members','project','task'),
        ('description', 'status', 'color'),
        ('start_date', 'end_date'),
        'budget',
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
