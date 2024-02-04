from django.core.management import BaseCommand

from mailing.cron import mailing_monthly_job


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailing_monthly_job()
        print("run mailing_monthly")
