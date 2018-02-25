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


# class TestSenderView:

#     def test_view_200(self, rf, db):
#         request = rf.get('/emailer/send')
#         view = views.trigger_email_sender
#         response = view(request)
#         assert response.status_code == 200

#     def test_calls_sender(self, rf, db):
#         request = rf.get('/emailer/send')
#         with patch('emailer.sender.sender') as mock_sender:
#             views.trigger_email_sender(request)
#             assert mock_sender.called


# class TestDashboardView:

#     def test_view_200(self, rf, db):
#         request = rf.get('/emailer/dashboard')
#         view = views.dashboard
#         response = view(request)
#         assert response.status_code == 200

#     @patch('emailer.views.render')
#     def test_passes_list_emailable_users(self, mock_render, django_user_model, rf, db):
#         make_users(django_user_model, state='A', last_email=YESTERDAY)
#         request = rf.get('/emailer/dashboard')
#         views.dashboard(request)
#         assert mock_render.called
#         assert len(mock_render.call_args[1]['context']['emailable_users']) > 0

#     @patch('emailer.views.render')
#     def test_passes_list_of_recent_email_events(self, mock_render, django_user_model, rf, db):
#         make_users(django_user_model, state='A', last_email=YESTERDAY)
#         request = rf.get('/emailer/dashboard')
#         views.dashboard(request)
#         assert mock_render.called
#         assert len(mock_render.call_args[1]['context']['email_events']) > 0


# class TestUserModelSignal:

#     def test_email_activity_created_after_user(self, rf, db):
#         User = get_user_model()
#         User.objects.get_or_create(first_name='testy')
#         assert models.EmailActivity.objects.count() == 1


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
            user_count = django_user_model.objects.filter(activity__state='A').count()
            assert user_count == 3




    
# class TestEmailEvent:

#     def test_created_when_email_sent(self, django_user_model):
#         make_users(django_user_model, state='A', last_email=YESTERDAY)
#         sender.sender(django_user_model)
#         assert models.EmailEvent.objects.count() == 1

#     def test_no_events_on_user_creation(self, django_user_model):
#         seeder.add_entity(django_user_model, 1)
#         assert models.EmailEvent.objects.count() == 0