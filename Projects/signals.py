from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Task, SubTask


@receiver(post_save, sender=Project)
def after_saving_project_create_template(sender, instance, created, **kwargs):
    if created:  # and instance.template is True:
        task = Task.objects.create(
            project=instance,
            title=f"{instance.title}/ Task",
            color=instance.color
        )
        SubTask.objects.create(
            task=task,
            title=f"{task.title}/ Subtask",
            color=instance.color
        )
