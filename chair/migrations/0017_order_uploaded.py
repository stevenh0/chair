# Generated by Django 2.0.5 on 2018-06-04 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chair', '0016_auto_20180604_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='uploaded',
            field=models.BooleanField(default=False),
        ),
    ]
