# Generated by Django 4.1 on 2023-01-01 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('My_App', '0044_session_message_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='bh',
        ),
    ]
