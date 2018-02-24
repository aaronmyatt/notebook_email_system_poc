from django.urls import path
from . import views

urlpatterns = [
    path(r'emailer/send', views.trigger_email_sender, name='email_sender'),
]