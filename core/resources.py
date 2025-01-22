# core/resources.py

from import_export import resources
from .models import Task

class TaskResource(resources.ModelResource):
    """
    Класс для экспорта/импорта модели Task через django-import-export
    """
    def get_export_queryset(self, request):
        return self._meta.model.objects.exclude(status='cancelled')

    def dehydrate_title(self, task_obj):
        return f"[Exported] {task_obj.title}"

    def get_project_title(self, task_obj):
        return task_obj.project.title if task_obj.project else ''

    class Meta:
        model = Task
        fields = (
            'id',
            'project_title',
            'title',
            'description',
            'status',
            'created_at',
            'deadline'
        )
        export_order = (
            'id',
            'project_title',
            'title',
            'description',
            'status',
            'created_at',
            'deadline'
        )