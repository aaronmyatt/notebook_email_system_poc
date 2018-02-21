from django.db import models
from django.contrib.auth import get_user_model

class EmailActivity(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name='emails',
        related_query_name='emails'
        )
    last_email = models.DateField(auto_now=True)

from .signals import *