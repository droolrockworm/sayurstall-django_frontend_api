# Generated by Django 2.0.4 on 2020-03-31 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0044_auto_20200331_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='measurement',
            field=models.CharField(choices=[('tiedbunch', 'Tied Bunch'), ('kg', 'Kg'), ('unit', 'Unity')], default='kg', max_length=100),
        ),
    ]
