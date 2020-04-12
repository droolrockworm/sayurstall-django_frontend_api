# Generated by Django 2.0.4 on 2020-04-07 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0048_auto_20200404_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='locations.Category'),
        ),
    ]
