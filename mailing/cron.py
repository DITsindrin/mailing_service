from .models import Mailing

from .services import my_send_mailing


def mailing_daily_job():
    """Crontab ежедневная рассылка"""
    mailings = Mailing.objects.all().filter(mailing_periodicity='Раз в день').exclude(is_active=False)
    if mailings.exists():
        for mailing in mailings:
            my_send_mailing(mailing)


def mailing_weekly_job():
    """Crontab еженедельная рассылка"""
    mailings = Mailing.objects.all().filter(mailing_periodicity='Раз в неделю').exclude(is_active=False)
    if mailings.exists():
        for mailing in mailings:
            my_send_mailing(mailing)


def mailing_monthly_job():
    """Crontab ежемесячная рассылка"""
    mailings = Mailing.objects.all().filter(mailing_periodicity='Раз в месяц').exclude(is_active=False)
    if mailings.exists():
        for mailing in mailings:
            my_send_mailing(mailing)
