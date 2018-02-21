from django.contrib.auth import get_user_model
from . import models
from . import views

def test_login_view(rf):
    request = rf.get('/login')
    view = views.LoginView.as_view()
    response = view(request)
    assert response.status_code == 200

class TestUserModelSignal:

    def test_user_activity_created_after_user(self, rf, db):
        User = get_user_model()
        User.objects.get_or_create(first_name='testy')
        assert models.UserActivity.objects.count() == 1