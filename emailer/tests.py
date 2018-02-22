from datetime import date, timedelta
import pytest
from mock import patch
from django.test import TestCase
from django_seed import Seed
from django.contrib.auth import get_user_model
from login.models import UserActivity
from . import models
from . import sender

seeder = Seed.seeder()

TODAY = date.today()
FOUR_DAYS_AGO = (date.today() - timedelta(4))
TWO_DAYS_AGO = (date.today() - timedelta(2))

def make_users(User, state='A', last_email=TODAY):
    seeder.add_entity(User, 3)
    seeder.execute()
    u = User.objects.first()
    s = u.activity.all()[0]
    s.state = state
    e = u.emails.all()[0]
    e.last_email = last_email
    s.save()
    e.save()

class TestUserModelSignal:

    def test_email_activity_created_after_user(self, rf, db):
        User = get_user_model()
        User.objects.get_or_create(first_name='testy')
        assert models.EmailActivity.objects.count() == 1


class TestEmailSender:


    class TestInactiveUsers:

        @patch('emailer.sender.send_emails')
        def test_does_not_recieve_email(self, mock_sender, django_user_model, db):
            make_users(django_user_model, state='I')
            sender.sender(django_user_model)
            assert mock_sender.called
            inactive_count = mock_sender.call_args[0][0].filter(activity__state='I').count()
            assert inactive_count == 0


    @patch('emailer.sender.send_emails')
    class TestNonResponsiveUsers:

        def test_gets_email_after_three_days(self, mock_sender, django_user_model, db):
            make_users(django_user_model, state='NR', last_email=FOUR_DAYS_AGO)
            sender.sender(django_user_model)
            assert mock_sender.called
            nr_count = mock_sender.call_args[0][0].filter(activity__state='NR').count()
            assert nr_count == 1

        def test_exluded_when_last_email_too_recent(self, mock_sender, django_user_model, db):
            make_users(django_user_model, state='NR', last_email=TWO_DAYS_AGO)
            sender.sender(django_user_model)
            assert mock_sender.called
            nr_count = mock_sender.call_args[0][0].filter(activity__state='NR').count()
            assert nr_count == 0



