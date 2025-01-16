from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer
from .filters import TaskFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Пример Q-запрос (1): находить пользователей,
    # у которых имя содержит 'abc' или 'xyz', И при этом email не начинается на 'test'
    @action(methods=['GET'], detail=False)
    def abc_or_xyz(self, request):
        qs = self.get_queryset().filter(
            (Q(name__icontains='abc') | Q(name__icontains='xyz')) &
            ~Q(email__startswith='test')
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    # Дополнительный метод: вернуть проекты, в названии которых есть 'django'
    @action(methods=['GET'], detail=False)
    def django_projects(self, request):
        qs = self.get_queryset().filter(title__icontains='django')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # Фильтрация через django-filters
    filterset_class = TaskFilter
    # Поиск по title или description
    search_fields = ['title', 'description']

    # Пример Q-запрос (2)
    # Ищем задачи, у которых status='done' ИЛИ (deadline < now)
    # но исключаем те, у которых title содержит 'cancel'
    @action(methods=['GET'], detail=False)
    def done_or_expired(self, request):
        from django.utils import timezone
        now = timezone.now()
        qs = self.get_queryset().filter(
            (Q(status='done') | Q(deadline__lt=now)) &
            ~Q(title__icontains='cancel')
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    # Пример @action (detail=True, POST): сменить статус задачи
    @action(methods=['POST'], detail=True)
    def change_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status', 'in_progress')
        task.status = new_status
        task.save()
        return Response({
            'status': 'Status updated',
            'task_id': task.id,
            'new_status': new_status
        })