# Generated by Django 4.1 on 2022-12-30 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('My_App', '0011_boardinghouse_power'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardinghouse',
            name='power',
        ),
    ]
