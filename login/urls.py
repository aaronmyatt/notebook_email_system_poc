from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.LoginView.as_view(), name='home'),
    path(r'login/', views.LoginView.as_view(), name='login')
]