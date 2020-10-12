import logging

from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taskmanager.models import Task, ChangeOfStatus, Notification, NotificationRecipient
from taskmanager.serializers import TaskSerializer
from taskmanager.tasks import send_notification


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.queryset.get(pk=kwargs.get('pk'))
        previous_status = instance.status
        next_status = data['status']
        serializer = self.serializer_class(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if previous_status != next_status:
            try:
                ChangeOfStatus.objects.create(
                    task=instance,
                    previous_status=previous_status,
                    next_status=next_status,
                    user=request.user
                )
            except IntegrityError as e:
                logging.warning(e.__str__())
        return Response(serializer.data)


@receiver(post_save, sender=ChangeOfStatus)
def change_of_status_post_save(sender, instance, **kwargs):
    task = instance.task
    try:
        n = Notification.objects.create(
            task=task,
            message='The task {} status was changed from {} to {}'.format(
                task.title,
                instance.previous_status,
                instance.next_status,
            )
        )
        for observer in task.observers.all():
            try:
                NotificationRecipient.objects.create(notification=n, recipient=observer)
            except IntegrityError as e:
                logging.warning(e.__str__())
        try:
            NotificationRecipient.objects.create(notification=n, recipient=task.executor)
        except IntegrityError as e:
            logging.warning(e.__str__())
    except IntegrityError as e:
        logging.warning(e.__str__())


@receiver(post_save, sender=NotificationRecipient)
def notification_post_save(sender, instance, **kwargs):
    send_notification.delay(instance.notification.id, instance.recipient.email)
