from django.contrib.auth import get_user_model
from . import models

class TestUserModelSignal:

    def test_email_activity_created_after_user(self, rf, db):
        User = get_user_model()
        User.objects.get_or_create(first_name='testy')
        assert models.EmailActivity.objects.count() == 1