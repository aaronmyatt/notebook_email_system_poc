import pytest
from mock import patch
from django.test import TestCase
from django_seed import Seed
from django.contrib.auth import get_user_model
from login.models import UserActivity
from . import models
from . import sender

seeder = Seed.seeder()

def make_users(User):
    seeder.add_entity(User, 3)
    seeder.execute()
    u = User.objects.first()
    s = u.activity.all()[0]
    s.state = 'I'
    s.save()

class TestUserModelSignal:

    def test_email_activity_created_after_user(self, rf, db):
        User = get_user_model()
        User.objects.get_or_create(first_name='testy')
        assert models.EmailActivity.objects.count() == 1


class TestEmailSender:

    @patch('emailer.sender.send_emails')
    def test_does_not_email_inactive_users(self, mock_sender, django_user_model, db):
        make_users(django_user_model)
        sender.sender(django_user_model)
        assert mock_sender.called
        inactive_count = mock_sender.call_args[0][0].filter(activity__state='I').count()
        assert inactive_count == 0