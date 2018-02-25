from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model

def trigger_updater(request):
    return HttpResponse()

def dashboard(request):
    return render(request, 'updater_dashboard.html', 
                  context=dict())