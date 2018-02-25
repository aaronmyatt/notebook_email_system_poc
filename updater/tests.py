from datetime import timedelta
import pytest
from mock import patch
from django.utils.timezone import now
from django_seed import Seed
from login.models import UserActivity
from . import models, views, user_updater

seeder = Seed.seeder()

NOW = now()
FIVE_DAYS_AGO = (NOW - timedelta(5))
FOUR_DAYS_AGO = (NOW - timedelta(4))
THREE_DAYS_AGO = (NOW - timedelta(3))
TWO_DAYS_AGO = (NOW - timedelta(2))
YESTERDAY = (NOW - timedelta(1))

def make_users(User, state='A', last_login=NOW):
    seeder.add_entity(User, 3, {
        'last_login': lambda x: NOW,
    })
    seeder.execute()
    u = User.objects.first()
    u.last_login = last_login
    u.save()
    u.activity.state = state
    u.activity.save()


class TestUpdaterView:

    def test_view_200(self, rf, db):
        request = rf.get('/updater/update')
        view = views.trigger_updater
        response = view(request)
        assert response.status_code == 200

    def test_calls_updater(self, rf, db):
        request = rf.get('/updater/update')
        with patch('updater.user_updater.updater') as mock_updater:
            views.trigger_updater(request)
            assert mock_updater.called


class TestDashboardView:

    def test_view_200(self, rf, db):
        request = rf.get('/updater/dashboard')
        view = views.dashboard
        response = view(request)
        assert response.status_code == 200

    @patch('updater.views.render')
    def test_passes_list_of_recent_update_events(self, mock_render, django_user_model, rf, db):
        make_users(django_user_model, state='A', last_login=FIVE_DAYS_AGO)
        request = rf.get('/updater/dashboard')
        views.dashboard(request)
        assert mock_render.called
        assert len(mock_render.call_args[1]['context']['update_events']) > 0


class TestUserUpdater:
    
    class TestActiveUsers:

        def test_4day_old_login_set_to_nonresponsive(self, django_user_model, db):
            make_users(django_user_model, last_login=FIVE_DAYS_AGO)
            user_updater.updater(UserActivity)
            user_count = django_user_model.objects.filter(activity__state='NR').count()
            assert user_count == 1

        def test_recent_logins_ignored(self, django_user_model, db):
            make_users(django_user_model, last_login=TWO_DAYS_AGO)
            user_updater.updater(UserActivity)
            user_count = django_user_model.objects.filter(activity__state='NR').count()
            assert user_count == 0

    class TestNonresponsiveUsers:

        def test_3day_old_login_set_to_inactive(self, django_user_model, transactional_db):
            make_users(django_user_model, state='NR', last_login=THREE_DAYS_AGO)
            user_updater.updater(UserActivity)
            user_count = django_user_model.objects.filter(activity__state='I').count()
            assert user_count == 1

        def test_recent_login_set_to_active(self, django_user_model, transactional_db):
            make_users(django_user_model, state='NR', last_login=YESTERDAY)
            user_updater.updater(UserActivity)
            user_count = django_user_model.objects.filter(activity__state='NR').count()
            assert user_count == 0

 
class TestEmailEvent:

    def test_created_when_email_sent(self, django_user_model):
        make_users(django_user_model, state='A', last_login=FIVE_DAYS_AGO)
        user_updater.updater(UserActivity)
        assert models.UserUpdateEvent.objects.count() == 1

    def test_no_events_on_user_activity_creation(self, django_user_model):
        seeder.add_entity(UserActivity, 1)
        assert models.UserUpdateEvent.objects.count() == 0