from django.db import models

from authentication.models import User

class Task(models.Model):
    """
    Model for task table
    """
    class TaskStatus(models.TextChoices):
        """
        Enum for task status
        """
        PENDING = 'PENDING'
        IN_PROGRESS = 'IN_PROGRESS'
        COMPLETED = 'COMPLETED'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices = TaskStatus, default = TaskStatus.PENDING, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
    REQUIRED_FIELDS = ['title', 'description']
