from django.db import models
from django.contrib.auth import get_user_model

class UserUpdateEvent(models.Model):
    publisher = models.OneToOneField(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name='event_publisher',
        related_query_name='publisher'
        )
    trigger_time = models.DateTimeField(auto_now_add=True)
    snapshot = models.TextField()

from .signals import *