from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User, Project, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # Пример валидации: имя не может быть пустым или слишком коротким
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError("Имя пользователя должно содержать минимум 3 символа.")
        return value


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    # Пример валидации: title не должен содержать слово "forbidden"
    def validate_title(self, value):
        if "forbidden" in value.lower():
            raise ValidationError("Название проекта не должно содержать слово 'forbidden'.")
        return value


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    # Пример валидации: нельзя ставить deadline в прошлом (упрощённо)
    def validate_deadline(self, value):
        from django.utils import timezone
        if value and value < timezone.now():
            raise ValidationError("Нельзя установить дедлайн в прошлом.")
        return value