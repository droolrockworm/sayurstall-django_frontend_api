# Generated by Django 2.0.4 on 2019-03-25 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0018_auto_20190325_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]