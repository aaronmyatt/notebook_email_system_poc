from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_seed import Seed

seeder = Seed.seeder()


TODAY = date.today()
FOUR_DAYS_AGO = (date.today() - timedelta(4))
YESTERDAY = (date.today() - timedelta(1))


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.create_one_active_user()
        self.create_one_non_responsive_user()

    def create_one_active_user(self):
        User = get_user_model()
        seeder.add_entity(User, 1)
        inserted_pks = seeder.execute().get(User)
        user = User.objects.filter(id__in=inserted_pks).all()[0]
        user.emails.last_email = YESTERDAY
        user.emails.save()
        return user

    def create_one_non_responsive_user(self):
        user = self.create_one_active_user()
        user.activity.state = 'NR'
        user.emails.last_email = FOUR_DAYS_AGO
        user.activity.save()
        user.emails.save()
        return user

