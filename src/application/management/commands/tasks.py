"""
application command.

This file contains the tasks command.
"""
from django.core.management.base import BaseCommand, CommandError
from config.celery import app


class Command(BaseCommand):
    help = 'Check for actively running Celery tasks'

    def handle(self, *args, **options):
        """
        Start the tasks command.

        :param args: *
        :param options: *
        :return: None
        """
        i = app.control.inspect()
        _, active = i.active().popitem()

        if len(active):
            raise CommandError('A task is currently running. Please do not shutdown the API.')
        else:
            self.stdout.write(self.style.SUCCESS('No tasks are currently running.'))
