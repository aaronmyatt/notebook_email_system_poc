from django.http import HttpResponse
from django.shortcuts import render
from . import sender
from django.contrib.auth import get_user_model

def trigger_email_sender(request):
    sender.sender(get_user_model())
    return HttpResponse()

def dashboard(request):
    return render(request, 'emailer_dashboard.html')