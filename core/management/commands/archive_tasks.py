from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Task

class Command(BaseCommand):
    help = "Archive tasks that are 'done' for more than 30 days (pseudo-archive)."

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=30)
        # Фильтр: задачи, у которых status='done' и created_at < cutoff
        old_done_tasks = Task.objects.filter(status='done', created_at__lt=cutoff)
        count = old_done_tasks.count()
        # Можно удалять, или менять статус на 'archived' (если бы у нас было такое поле).
        old_done_tasks.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Archived (deleted) {count} old 'done' tasks older than 30 days."
        ))