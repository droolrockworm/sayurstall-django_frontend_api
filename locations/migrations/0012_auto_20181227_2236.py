# Generated by Django 2.0.4 on 2018-12-27 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0011_auto_20181227_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='new_proxy',
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]