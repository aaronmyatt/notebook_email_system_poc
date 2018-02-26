from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from . import sender, models
from django.contrib.auth import get_user_model

@login_required
def trigger_email_sender(request):
    sender.sender(get_user_model())
    return HttpResponse()

@login_required
def dashboard(request):
    users = sender.emailable_users(get_user_model())
    events = models.EmailEvent.objects.all().order_by('-trigger_time')[:10]
    return render(request, 'emailer_dashboard.html', 
                  context=dict(emailable_users=users.all(), email_events=events))