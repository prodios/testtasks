from django.contrib.auth.models import User
from rest_framework import serializers

from taskmanager.models import Task, TaskItem


class TaskItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskItem
        fields = ['id', 'order', 'name', 'is_completed']


class TaskSerializer(serializers.ModelSerializer):
    items = TaskItemSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'executor',
            'observers',
            'status',
            'start_timestamp',
            'completion_timestamp',
            'planned_completion_timestamp',
            'items',
        ]

    def create(self, validated_data):
        items = validated_data.pop('items')
        observers = validated_data.pop('observers')
        task = Task.objects.create(**validated_data)

        for item in items:
            TaskItem.objects.create(task=task, **item)

        for observer in observers:
            task.observers.add(User.objects.get(username=observer))

        return task

    def update(self, instance, validated_data):
        items = validated_data.pop('items')
        updated_items = list()
        for item in items:
            task_item = TaskItem.objects.update_or_create(task=instance, order=item.pop('order'), defaults=item)[0]
            updated_items.append(task_item.id)
        TaskItem.objects.filter(task=instance).exclude(id__in=updated_items).delete()

        observers = validated_data.pop('observers')
        instance.observers.clear()
        for observer in observers:
            instance.observers.add(User.objects.get(username=observer))

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
