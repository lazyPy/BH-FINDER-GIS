# Generated by Django 4.1 on 2022-09-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('My_App', '0045_remove_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardinghouse',
            name='picture1',
            field=models.FileField(default='bh-default.png', upload_to='bh-images/'),
        ),
        migrations.AlterField(
            model_name='boardinghouse',
            name='picture2',
            field=models.FileField(default='bh-default.png', upload_to='bh-images/'),
        ),
        migrations.AlterField(
            model_name='boardinghouse',
            name='picture3',
            field=models.FileField(default='bh-default.png', upload_to='bh-images/'),
        ),
    ]
