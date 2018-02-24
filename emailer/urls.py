from django.urls import path
from . import views

urlpatterns = [
    path(r'emailer/send', views.trigger_email_sender, name='email_sender'),
    path(r'emailer/dashboard', views.dashboard, name='email_dashboard'),
]