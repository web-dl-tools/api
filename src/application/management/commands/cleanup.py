"""
application command.

This file contains the cleanup command.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone

from src.user.models import User, Log

class Command(BaseCommand):
    help = 'Perform maintenance cleanup'

    def handle(self, *args, **options):
        """
        Start the cleanup command.

        :param args: *
        :param options: *
        :return: None
        """
        self.stdout.write("Starting cleanup...")

        users = User.objects.all()
        for user in users:
            self.stdout.write(f"Processing user '{user.username}'...")
            self.__clean_logs(user)

        self.stdout.write(self.style.SUCCESS("Finished cleanup."))

    def __clean_logs(self, user: User) -> None:
        """
        Cleanup outdated logs for the given user.

        :param user: The user to cleanup for.
        :return: None
        """
        self.stdout.write("Cleaning outdated logs...")

        dt = timezone.localtime()
        end = dt.replace(hour=0, minute=0, second=0, microsecond=0)

        logs = Log.objects.filter(user=user, created_at__lte=end).order_by('-created_at')
        for log in logs:
            log.delete()

        self.stdout.write("Finished cleaning outdated logs.")
