# Generated by Django 4.2.6 on 2024-06-13 11:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0015_event_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
