# Generated by Django 4.1 on 2022-10-06 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_App', '0050_boardinghouse_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardinghouse',
            name='picture1',
            field=models.FileField(default=1, upload_to='bh-images/'),
            preserve_default=False,
        ),
    ]
