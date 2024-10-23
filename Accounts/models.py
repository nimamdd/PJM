from django.db import models
from django.contrib.auth.models import User
from Projects.models import Project, Task, SubTask
from Financial.models import FinancialRecord


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, unique=True)
    image = models.ImageField(upload_to='accounts/profile/',
                              default='accounts/profile/defualt/default_avatar.jpg')

    def __str__(self):
        return f'{self.user.username}'

    @property
    def project_counter(self):
        return Project.objects.filter(user=self.user).count()

    @property
    def project_percentage_done(self):
        if self.project_counter == 0:
            return 0
        done_projects = Project.objects.filter(user=self.user, status=True).count()
        return (done_projects / self.project_counter) * 100

    @property
    def task_counter(self):
        return Task.objects.filter(project__user=self.user).count()

    @property
    def task_percentage_done(self):
        if self.task_counter == 0:
            return 0
        done_task = Task.objects.filter(project__user=self.user, status=True).count()
        return (done_task / self.task_counter) * 100

    @property
    def subtask_counter(self):
        return SubTask.objects.filter(task__project__user=self.user).count()

    @property
    def subtask_percentage_done(self):
        if self.subtask_counter == 0:
            return 0
        done_subtask = SubTask.objects.filter(task__project__user=self.user, status=True).count()
        return (done_subtask / self.subtask_counter) * 100

    @property
    def count_all_financial_record(self):
        return FinancialRecord.objects.filter(who_created=self.user).count()

    @property
    def how_many_paid(self):
        all_financial = FinancialRecord.objects.filter(who_created=self.user, status__exact='paid')
        count = 0
        for f in all_financial:
            count += f.price
        return count


    @property
    def how_many_in_progress(self):
        all_financial = FinancialRecord.objects.filter(who_created=self.user, status__exact='in progress')
        count = 0
        for f in all_financial:
            count += f.price
        return count

    @property
    def how_many_canceled(self):
        all_financial = FinancialRecord.objects.filter(who_created=self.user, status__exact='canceled')
        count = 0
        for f in all_financial:
            count += f.price
        return count
