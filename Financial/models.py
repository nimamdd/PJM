from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class FinancialRecord(models.Model):
    STATUS_CHOICES = (
        ('paid', 'paid'),
        ('in progress', 'in progress'),
        ('canceled', 'canceled'),
    )
    who_created = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    price = models.FloatField()
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    create = models.DateTimeField()
    update = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title

    @property
    def kind(self):
        option = ['project', 'task', 'subtask']
        content_type = self.content_type
        if content_type.model == 'project':
            return option[0]
        elif content_type.model == 'task':
            return option[1]
        elif content_type.model == 'subtask':
            return option[2]
        return f'{content_type.model}'
