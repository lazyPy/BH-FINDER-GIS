# Generated by Django 4.1 on 2022-09-28 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_App', '0034_remove_boardinghouse_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardinghouse',
            name='picture',
            field=models.ImageField(blank=True, upload_to='bh-images/'),
        ),
    ]
