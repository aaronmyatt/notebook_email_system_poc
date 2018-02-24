from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import EmailActivity, EmailEvent


@receiver(post_save, sender=get_user_model())
def user_created_handler(sender, **kwargs):
    if kwargs.get('created', None):
        EmailActivity.objects.get_or_create(user=kwargs.get('instance'))

@receiver(post_save, sender=EmailActivity)
def email_activity_saved_handler(sender, **kwargs):
    if not kwargs.get('created', None):
        EmailEvent.objects.get_or_create(publisher=kwargs.get('instance'))