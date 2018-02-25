from django.http import HttpResponse
from django.shortcuts import render
from login.models import UserActivity
from . import user_updater, models

def trigger_updater(request):
    user_updater.updater(UserActivity)
    return HttpResponse()

def dashboard(request): 
    events = models.UserUpdateEvent.objects.all().order_by('-trigger_time')[:10]
    return render(request, 'updater_dashboard.html', 
                  context=dict(update_events=events))