import logging

from django.core.mail import send_mail
from django.db import IntegrityError
from django.utils import timezone

from taskmanager.models import Task, Notification, NotificationRecipient
from testtasks.celery import app
from testtasks.settings import EMAIL_HOST_USER


@app.task()
def check_tasks():
    for overdue_task in Task.objects.filter(
            planned_completion_timestamp__lt=timezone.now()).exclude(status=Task.Status.completed):
        try:
            n = Notification.objects.create(
                task=overdue_task,
                message='The task "{}" was overdue'.format(overdue_task.title)
            )
            try:
                NotificationRecipient.objects.create(notification=n, recipient=overdue_task.executor)
            except IntegrityError as e:
                logging.warning(e.__str__())
        except IntegrityError as e:
            logging.warning(e.__str__())


@app.task()
def send_notification(notification_id, recipient_email):
    notification = Notification.objects.get(id=notification_id)
    send_mail(
        notification.task.title,
        notification.message,
        EMAIL_HOST_USER,
        [recipient_email],
        fail_silently=False,
    )
