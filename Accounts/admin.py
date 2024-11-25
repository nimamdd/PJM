from django.contrib import admin
from .models import Profile , Team
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'image_thumbnail')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    list_per_page = 10


#@admin_thumbnails.thumbnail('image')
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner','id')
    # list_filter = ('username', 'email')
    # search_fields = ('username', 'email')
    # list_per_page = 10

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team, TeamAdmin)
