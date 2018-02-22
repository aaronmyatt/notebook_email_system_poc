from django.db import models
from django.contrib.auth import get_user_model

class UserActivity(models.Model):
    USER_STATES = (
        ('A', 'Active'),
        ('NR', 'None Responsive'),
        ('I', 'Inactive'),
    )

    user = models.OneToOneField(
        get_user_model(), 
        on_delete=models.DO_NOTHING,
        related_name='activity',
        related_query_name='activity'
        )
    state = models.CharField(max_length = 1, choices=USER_STATES, default='A')

    @property
    def last_login(self):
        self.user.last_login

from .signals import *