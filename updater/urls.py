from django.urls import path
from . import views

urlpatterns = [
    path(r'updater/update', views.trigger_updater, name='trigger_update'),
    path(r'updater/dashboard', views.dashboard, name='updater_dashboard')
]