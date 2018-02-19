from . import views

def test_login_view(rf):
    request = rf.get('/login')
    view = views.LoginView.as_view()
    response = view(request)
    assert response.status_code == 200

