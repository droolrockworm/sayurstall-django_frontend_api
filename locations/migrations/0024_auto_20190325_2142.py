# Generated by Django 2.0.4 on 2019-03-25 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0023_userprofile_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.BooleanField(default=False, help_text='Permission to use mobile app'),
        ),
    ]
