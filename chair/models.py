from django.db import models


# Create your models here.
class OrderStatus(models.Model):
    auto_fulfill = models.BooleanField()
    last_update = models.CharField()


class Customer(models.Model):
    customer_id = models.CharField()
    firstname = models.CharField()
    lastname = models.CharField()
    county = models.CharField()
    phone = models.CharField()
    state = models.CharField()
    street = models.CharField()
    zip = models.CharField()


class Order(models.Model):
    order_id = models.CharField()
    status = models.CharField()
    shipped = models.BooleanField()
    tracking_id = models.CharField()
    customer_id = models.ForeignKey('Customer')
