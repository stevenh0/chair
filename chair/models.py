from django.db import models


# Create your models here.
class OrderStatus(models.Model):
    auto_fulfill = models.BooleanField()
    last_update = models.CharField()


class Customer(models.Model):
    pass


class Order(models.Model):
    status = models.CharField()
    shipped = models.BooleanField()
    tracking_id = models.CharField()
    customer_id = models.ForeignKey('Customer')
