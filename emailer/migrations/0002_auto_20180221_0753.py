# Generated by Django 2.0.2 on 2018-02-21 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emailer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailactivity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='emails', related_query_name='emails', to=settings.AUTH_USER_MODEL),
        ),
    ]
