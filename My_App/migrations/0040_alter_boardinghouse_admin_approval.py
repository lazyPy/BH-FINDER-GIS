# Generated by Django 4.1 on 2022-09-28 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_App', '0039_remove_boardinghouse_admin_approve_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardinghouse',
            name='admin_approval',
            field=models.CharField(blank=True, choices=[('APPROVED', 'APPROVED'), ('DENIED', 'DENIED')], max_length=200),
        ),
    ]
