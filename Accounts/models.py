from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
import uuid
from Financial.models import FinancialRecord
from Projects.models import Project,Task,SubTask


class ProfileManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The email number field must be set')
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)


class Profile(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    image = models.ImageField(upload_to='accounts/profile/', default='accounts/profile/default/default_avatar.jpg')
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    teams = models.ManyToManyField('Team',null=True, blank=True, related_name='profile_teams')
    objects = ProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    def has_perm(self, perm, obj=None):
        """"""
        return True

    def has_module_perms(self, app_label):
        """

        """
        return True

    def __str__(self):
        return f'{self  .username}'

    @property
    def project_counter(self):
        return Project.objects.filter(owner=self).count()

    @property
    def project_percentage_done(self):
        if self.project_counter == 0:
            return 0
        done_projects = Project.objects.filter(user=self, status=True).count()
        return (done_projects / self.project_counter) * 100

    @property
    def task_counter(self):
        return Task.objects.filter(project__owner=self).count()

    @property
    def task_percentage_done(self):
        if self.task_counter == 0:
            return 0
        done_task = Task.objects.filter(project__owner=self, status=True).count()
        return (done_task / self.task_counter) * 100

    @property
    def subtask_counter(self):
        return SubTask.objects.filter(task__project__owner=self).count()

    @property
    def subtask_percentage_done(self):
        if self.subtask_counter == 0:
            return 0
        done_subtask = SubTask.objects.filter(task__project__owner=self, status=True).count()
        return (done_subtask / self.subtask_counter) * 100

    @property
    def count_all_financial_record(self):
        return FinancialRecord.objects.filter(who_created=self).count()

    @property
    def how_many_paid(self):
        all_financial = FinancialRecord.objects.filter(who_created=self, status__exact='paid')
        count = 0
        for f in all_financial:
            count += f.price
        return count


    @property
    def how_many_in_progress(self):
        all_financial = FinancialRecord.objects.filter(who_created=self, status__exact='in progress')
        count = 0
        for f in all_financial:
            count += f.price
        return count

    @property
    def how_many_canceled(self):
        all_financial = FinancialRecord.objects.filter(who_created=self, status__exact='canceled')
        count = 0
        for f in all_financial:
            count += f.price
        return count



class Team(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='accounts/teams/', default='accounts/teams/default/defalt_avatar.png')
    descriptions = models.TextField(default='', blank=True)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='owner_team')
    admin = models.ManyToManyField(Profile,  related_name='admin_team', blank=True)
    members = models.ManyToManyField(Profile, related_name='members_team')
    projects = models.ManyToManyField('Projects.Task', related_name='team_projects',null=True, blank=True)

    def __str__(self):
        return self.name

