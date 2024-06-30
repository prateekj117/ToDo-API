from rest_framework import serializers

from todo.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'user']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
