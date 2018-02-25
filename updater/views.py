from django.http import HttpResponse
from django.shortcuts import render
from login.models import UserActivity
from . import user_updater

def trigger_updater(request):
    user_updater.updater(UserActivity)
    return HttpResponse()

def dashboard(request):
    return render(request, 'updater_dashboard.html', 
                  context=dict())