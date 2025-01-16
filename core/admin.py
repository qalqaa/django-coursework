from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .models import User, Project, Task
from .resources import TaskResource

@admin.register(User)
class UserAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'email', 'date_joined')
    search_fields = ('name', 'email')
    fields = ('name', 'email', 'password', 'date_joined')
    readonly_fields = ('date_joined',)


@admin.register(Project)
class ProjectAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    fields = ('title', 'description', 'author', 'created_at')
    readonly_fields = ('created_at',)


class TaskAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = TaskResource
    list_display = ('id', 'title', 'project_link', 'short_desc', 'status', 'created_at', 'deadline')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    fields = ('project', 'title', 'description', 'status', 'created_at', 'deadline')

    readonly_fields = ('created_at',)

    # Переопределяем форматы экспорта
    def get_export_formats(self):
        formats = [
            base_formats.CSV,
            base_formats.XLSX,  # требует openpyxl
            base_formats.JSON,
            # base_formats.YAML (если нужен, установить pyyaml)
        ]
        return [f for f in formats if f().can_export()]

    def project_link(self, obj):
        return obj.project.title if obj.project else '-'
    project_link.short_description = 'Project'

    def short_desc(self, obj):
        return (obj.description[:30] + '...') if obj.description else '-'
    short_desc.short_description = 'Short desc'

admin.site.register(Task, TaskAdmin)