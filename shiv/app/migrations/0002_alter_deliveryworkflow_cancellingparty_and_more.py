# Generated by Django 4.0.5 on 2022-06-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryworkflow',
            name='cancellingParty',
            field=models.CharField(blank=True, choices=[('customer', 'Customer'), ('seller', 'Seller')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryworkflow',
            name='partyAtFault',
            field=models.CharField(blank=True, choices=[('customer', 'Customer'), ('seller', 'Seller')], max_length=30, null=True),
        ),
        migrations.DeleteModel(
            name='Party',
        ),
    ]
