# Generated by Django 2.0.4 on 2018-07-10 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_auto_20180707_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='new_proxy',
            field=models.BooleanField(default=False),
        ),
    ]