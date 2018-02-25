import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from login.models import UserActivity
from . import models


@receiver(post_save, sender=UserActivity)
def email_activity_saved_handler(sender, **kwargs):
    if not kwargs.get('created', None):
        snapshot = kwargs['instance'].__dict__.copy()
        snapshot.pop('_state')
        models.UserUpdateEvent.objects.get_or_create(
            publisher=kwargs.get('instance').user,
            snapshot=json.dumps(snapshot)
        )