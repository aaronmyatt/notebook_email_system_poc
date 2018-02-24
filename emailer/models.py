from django.db import models
from django.contrib.auth import get_user_model

class EmailActivity(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name='emails',
        related_query_name='emails'
        )
    last_email = models.DateField(auto_now_add=True)


class EmailEvent(models.Model):
    publisher = models.OneToOneField(
        EmailActivity,
        on_delete=models.DO_NOTHING,
        related_name='event_publisher',
        related_query_name='publisher'
        )
    trigger_time = models.DateTimeField(auto_now_add=True)

from .signals import *