# Generated by Django 4.1 on 2022-11-26 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_App', '0008_alter_boardinghouse_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardinghouse',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
