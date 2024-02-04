from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='DITsi@mail.ru',
            first_name='Admin',
            last_name='MailingService',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('01906002')
        user.save()
