# Generated by Django 2.0.2 on 2018-02-22 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20180221_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='activity', related_query_name='activity', to=settings.AUTH_USER_MODEL),
        ),
    ]