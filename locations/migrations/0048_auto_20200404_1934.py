# Generated by Django 2.0.4 on 2020-04-04 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0047_auto_20200404_0616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='unit_price',
            new_name='price_per_kg',
        ),
        migrations.RemoveField(
            model_name='product',
            name='measurement',
        ),
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='date_fulfilled',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='date_payed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='estimated_total',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price_per_tied_bunch',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price_per_unit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='additional',
            field=models.TextField(blank=True, null=True),
        ),
    ]
