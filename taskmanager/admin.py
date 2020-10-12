from django.contrib import admin

from taskmanager.models import Task, TaskItem, ChangeOfStatus, Notification

admin.site.register(Task)
admin.site.register(TaskItem)
admin.site.register(ChangeOfStatus)
admin.site.register(Notification)
