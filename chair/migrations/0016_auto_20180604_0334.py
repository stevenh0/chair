# Generated by Django 2.0.5 on 2018-06-04 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chair', '0015_auto_20180601_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bestbuy_commission',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
