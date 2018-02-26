from datetime import date, timedelta
import pytest
from mock import patch
from django.test import TestCase
from django_seed import Seed
from django.contrib.auth import get_user_model
from login.models import UserActivity
from . import models, views, sender

seeder = Seed.seeder()

TODAY = date.today()
FOUR_DAYS_AGO = (date.today() - timedelta(4))
TWO_DAYS_AGO = (date.today() - timedelta(2))
YESTERDAY = (date.today() - timedelta(1))

def make_users(User, state='A', last_email=TODAY):
    seeder.add_entity(User, 3)
    seeder.execute()
    u = User.objects.first()
    u.activity.state = state
    u.activity.save()
    u.emails.last_email = last_email
    u.emails.save()


class TestSenderView:
    def test_view_200(self, admin_client):
        response = admin_client.get('/emailer/send')
        assert response.status_code == 200
    def test_calls_sender(self, admin_client):
        with patch('emailer.sender.sender') as mock_sender:
            admin_client.get('/emailer/send')
            assert mock_sender.called


class TestDashboardView:

    def test_view_200(self, admin_client):
        response = admin_client.get('/emailer/dashboard')
        assert response.status_code == 200

    @patch('emailer.views.render')
    def test_passes_list_emailable_users(self, mock_render, django_user_model, rf, db, admin_user):
        make_users(django_user_model, state='A', last_email=YESTERDAY)
        request = rf.get('/emailer/dashboard')
        request.user = admin_user
        views.dashboard(request)
        assert mock_render.called
        assert len(mock_render.call_args[1]['context']['emailable_users']) > 0

    @patch('emailer.views.render')
    def test_passes_list_of_recent_email_events(self, mock_render, django_user_model, rf, db, admin_user):
        make_users(django_user_model, state='A', last_email=YESTERDAY)
        request = rf.get('/emailer/dashboard')
        request.user = admin_user
        views.dashboard(request)
        assert mock_render.called
        assert len(mock_render.call_args[1]['context']['email_events']) > 0


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


    class TestNonResponsiveUsers:

        @patch('emailer.sender.send_emails')
        def test_gets_email_after_three_days(self, mock_sender, django_user_model, db):
            make_users(django_user_model, state='NR', last_email=FOUR_DAYS_AGO)
            sender.sender(django_user_model)
            assert mock_sender.called
            nr_count = mock_sender.call_args[0][0].filter(activity__state='NR').count()
            assert nr_count == 1

        @patch('emailer.sender.send_emails')
        def test_exluded_when_last_email_too_recent(self, mock_sender, django_user_model, db):
            make_users(django_user_model, state='NR', last_email=TWO_DAYS_AGO)
            sender.sender(django_user_model)
            assert mock_sender.called
            nr_count = mock_sender.call_args[0][0].filter(activity__state='NR').count()
            assert nr_count == 0

        def test_recieves_email_only_once_three_daily(self, django_user_model, db):
            make_users(django_user_model, state='NR', last_email=FOUR_DAYS_AGO)
            sender.sender(django_user_model)
            user_count = django_user_model.objects.filter(emails__last_email__lt=TODAY).count()
            assert user_count == 0

    
    class TestActiveUsers:

        @patch('emailer.sender.send_emails')
        def test_recieves_email_every_day(self, mock_sender, django_user_model, db):
            make_users(django_user_model, state='A', last_email=YESTERDAY)
            sender.sender(django_user_model)
            assert mock_sender.called
            inactive_count = mock_sender.call_args[0][0].filter(activity__state='A').count()
            assert inactive_count == 1

        def test_recieves_email_only_once_daily(self, django_user_model, db):
            make_users(django_user_model, state='A', last_email=TODAY)
            sender.sender(django_user_model)
            user_count = django_user_model.objects.filter(emails__last_email__lt=TODAY).count()
            assert user_count == 0


class TestEmailEvent:

    def test_created_when_email_sent(self, django_user_model):
        make_users(django_user_model, state='A', last_email=YESTERDAY)
        sender.sender(django_user_model)
        assert models.EmailEvent.objects.count() == 1

    def test_no_events_on_user_creation(self, django_user_model):
        seeder.add_entity(django_user_model, 1)
        assert models.EmailEvent.objects.count() == 0