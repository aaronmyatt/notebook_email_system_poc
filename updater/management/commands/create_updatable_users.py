from datetime import date, timedelta
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_seed import Seed

seeder = Seed.seeder()


NOW = now()
SIX_DAYS_AGO = (NOW - timedelta(5))
FIVE_DAYS_AGO = (NOW - timedelta(5))
FOUR_DAYS_AGO = (NOW - timedelta(4))
YESTERDAY = (NOW - timedelta(1))


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.create_one_active_user()
        self.create_one_inactive_non_responsive_user()
        self.create_one_active_non_responsive_user()

    def create_one_active_user(self):
        User = get_user_model()
        seeder.add_entity(User, 1)
        inserted_pks = seeder.execute().get(User)
        user = User.objects.filter(id__in=inserted_pks).all()[0]
        user.last_login = FIVE_DAYS_AGO
        user.save()
        return user

    def create_one_inactive_non_responsive_user(self):
        user = self.create_one_active_user()
        user.last_login = SIX_DAYS_AGO
        user.save()
        return user

    def create_one_active_non_responsive_user(self):
        user = self.create_one_active_user()
        user.last_login = YESTERDAY
        user.save()