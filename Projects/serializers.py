from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Accounts.models import Team,Profile
from Accounts.serializers import ProfileSerializers
from .models import Project, Task, SubTask


class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'pk',
            'title',
            'owner',
            'description',
            'color',
            'image',
            'start_date',
            'end_date',
            'status',
            'budget',
            'content_id',

        )
        extra_kwargs = {
            'user': {'read_only': True},
        }


class TaskSerializer(serializers.ModelSerializer):
    admins = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=True)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        model = Task
        fields = [
            'pk',
            'project',
            'team',
            'title',
            'image',
            'color',
            'description',
            'budget',
            'start_date',
            'end_date',
            'admins',
            'status',
            'content_id',
        ]
        depth = 1
        extra_kwargs = {
            'project': {'read_only': True},
        }

    def validate_admins(self, value):
        team = self.initial_data.get('team')  # دریافت تیم از داده‌های اولیه
        if team:
            team_instance = Team.objects.get(id=team)
            team_admins = team_instance.admin.all()

            for admin in value:
                if admin not in team_admins:
                    raise ValidationError(f'{admin} is not an admin of the selected team.')
        return value

    def create(self, validated_data):
        # تیم از validated_data گرفته می‌شود
        team_data = validated_data.get('team')
        task = Task.objects.create(**validated_data)  # تسک ایجاد می‌شود
        # برای ManyToMany نیازی به set() نیست، چون این فیلد به صورت خودکار ذخیره می‌شود.
        return task



class SubtaskSerializers(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), many=True)
    class Meta:
        model = SubTask
        fields = [
            'pk',
            'task',
            'title',
            'image',
            'color',
            'description',
            'budget',
            'start_date',
            'end_date',
            'status',
            'content_id',
            'members',
        ]
        depth = 2
        extra_kwargs = {
            'task': {'read_only': True},
        }
