# Generated by Django 2.0.5 on 2018-05-19 23:16

from django.db import migrations


def create_order_status(apps, schema_editor):
    order_status = apps.get_model("chair", "OrderStatus")
    order_status.objects.create(auto_fulfill=False)


class Migration(migrations.Migration):

    dependencies = [
        ('chair', '0006_order_newegg_feed'),
    ]

    operations = [
        migrations.RunPython(create_order_status, reverse_code=migrations.RunPython.noop)
    ]