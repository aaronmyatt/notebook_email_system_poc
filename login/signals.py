from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserActivity


@receiver(post_save, sender=get_user_model())
def webinar_created_handler(sender, **kwargs):
    if kwargs.get('created', None):
        UserActivity.objects.get_or_create(user=kwargs.get('instance'))