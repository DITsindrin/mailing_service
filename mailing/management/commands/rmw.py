from django.core.management import BaseCommand

from mailing.cron import mailing_weekly_job


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailing_weekly_job()
        print("run mailing_weekly")
