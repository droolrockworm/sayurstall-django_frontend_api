# Generated by Django 2.0.4 on 2019-03-25 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0019_userprofile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='company',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]