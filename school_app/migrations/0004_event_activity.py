# Generated by Django 4.1.1 on 2023-08-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school_app", "0003_rename_events_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="activity",
            field=models.ImageField(default="", upload_to="activity/images"),
        ),
    ]
