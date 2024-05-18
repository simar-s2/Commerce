# Generated by Django 5.0.4 on 2024-05-18 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_remove_bid_listing_alter_bid_bid_alter_listing_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_bid', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]