from django.core.management import BaseCommand

from mailing.cron import mailing_daily_job


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailing_daily_job()
        print("run mailing_daily")
