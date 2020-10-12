from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):

    class Status(models.IntegerChoices):
        planned = 0, 'Планируется'
        active = 1, 'Активная'
        control = 2, 'Контроль'
        completed = 3, 'Завершена'

    title = models.CharField(max_length=256)
    description = models.TextField()
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    observers = models.ManyToManyField(User, related_name='observed_tasks')
    status = models.IntegerField(default=Status.planned, choices=Status.choices)
    start_timestamp = models.DateTimeField(blank=True, null=True)
    completion_timestamp = models.DateTimeField(blank=True, null=True)
    planned_completion_timestamp = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tasks'
        ordering = ['planned_completion_timestamp']


class TaskItem(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='items')
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=128)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task, self.name}'

    class Meta:
        db_table = 'task_items'
        ordering = ['task', 'order']
        unique_together = ['task', 'order']


class ChangeOfStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='status_changes')
    previous_status = models.IntegerField()
    next_status = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='status_changes')

    def __str__(self):
        return f'{self.user, self.task}'

    class Meta:
        db_table = 'status_changes'
        ordering = ['task', 'previous_status', 'next_status']


class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    recipients = models.ManyToManyField(User, through='NotificationRecipient', related_name='notifications')

    def __str__(self):
        return f'{self.task, self.message}'

    class Meta:
        db_table = 'notifications'
        ordering = ['task', 'message']


class NotificationRecipient(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notification_recipients'
        unique_together = ['notification', 'recipient']
