# Generated by Django 2.0.5 on 2018-05-18 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chair', '0003_auto_20180518_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='received',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]