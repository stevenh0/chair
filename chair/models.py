from django.db import models


# Create your models here.
class OrderStatus(models.Model):
    auto_fulfill = models.BooleanField()
    last_update = models.CharField(max_length=100, blank=True, null=True)


class Customer(models.Model):
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)


class Order(models.Model):
    order_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    received = models.CharField(max_length=100, blank=True, null=True)
    part_number = models.CharField(max_length=100, blank=True, null=True)
