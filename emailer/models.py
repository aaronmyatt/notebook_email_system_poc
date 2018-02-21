from django.db import models
from django.contrib.auth import get_user_model

class EmailActivity(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    last_email = models.DateField(auto_now=True)

from .signals import *