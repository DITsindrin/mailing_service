import datetime
from smtplib import SMTPException
import pytz
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mailing.models import Mailing, MailingLogs


def my_send_mailing(mailing):
    """Отправка писем по рассылкам и запись логов"""
    zon = pytz.timezone(settings.TIME_ZONE)
    # current_time = datetime.time(tzinfo=zon)
    current_time = datetime.datetime.now(zon).time()

    if mailing.start_time <= current_time < mailing.end_time:
        mailing.mailing_status = Mailing.LAUNCHED
        mailing.save()
        message = mailing.message_set.all()[0]
        for client in mailing.client.all():
            print(client)
            try:
                send_mailing = send_mail(
                    subject=message.letter_subject,
                    message=message.body_letter,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                log = MailingLogs(
                    last_try=mailing.start_time,
                    attempt_status=send_mailing,
                    error_msg='Сообщение успешно отправлено',
                    client=f'{client.email}',
                    mailing_settings=f'{mailing.title}',
                )
                log.save()

            except SMTPException as error:
                log = MailingLogs(
                    last_try=mailing.start_time,
                    attempt_status=False,
                    error_msg=f'Сообщение не отправлено, ошибка - {error}',
                    client=f'{client.email}',
                    mailing_settings=f'{mailing.title}',
                )
                log.save()

    else:
        print('Не совпало время')
        mailing.mailing_status = Mailing.COMPLETED
        mailing.save()
