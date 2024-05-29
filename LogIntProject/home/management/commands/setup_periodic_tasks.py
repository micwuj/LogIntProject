from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Sets up periodic tasks'

    def handle(self, *args, **options):
        task_name = 'Pull Data Every 10 Minutes'
        if not PeriodicTask.objects.filter(name=task_name).exists():
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=10,
                period=IntervalSchedule.MINUTES,
            )

            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name='Pull Data Every 10 Minutes',
                task='home.tasks.pull_data_from_active_resources_scheduled'
            )
            self.stdout.write(self.style.SUCCESS('Successfully set up periodic tasks'))
