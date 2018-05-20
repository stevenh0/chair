from secrets import BESTBUY_KEY
from chair.product_info import PRODUCT_INFO
from chair.models import Order, Customer

import requests
import json


# date should be in format yyyy-MM-dd
def grab_orders(date=None):
    headers = {'Authorization': BESTBUY_KEY}
    r = requests.get('https://marketplace.bestbuy.ca/api/orders',
                     {"start_date": date, "paginate": False}, headers=headers)
    r_data = json.loads(r.content)
    orders = r_data.get('orders')
    for order in orders:
        # grab necessary fields for newegg stuff and enter them into the db
        load_order(order)
    return len(orders)


# fill in information needed for an order
def load_order(order_info):
    for item in order_info.get('order_lines'):
        product_name = item.get('product_title')
        order, created = Order.objects.get_or_create(
            order_id=order_info.get('order_id'), product_name=product_name)
        customer = update_customer_info(order_info.get('customer'))
        order.customer_id = customer
        order.status = order_info.get('order_state')
        order.tracking_id = order_info.get('shipping_tracking')
        order.quantity = item.get('quantity')
        order.received = order_info.get('created_date')
        try:
            order.part_number = PRODUCT_INFO.get(product_name)[1]
        except:
            pass
        order.save()


def update_customer_info(customer_info):
    customer, created = Customer.objects.get_or_create(
        customer_id=customer_info.get('customer_id'))
    customer.firstname = customer_info.get('firstname')
    customer.lastname = customer_info.get('lastname')
    try:
        customer.country = customer_info['shipping_address'].get('country')
        customer.city = customer_info['shipping_address'].get('city')
        customer.phone = customer_info['shipping_address'].get('phone')
        customer.state = customer_info['shipping_address'].get('state')
        customer.street = customer_info['shipping_address'].get('street_1')
        customer.zip = customer_info['shipping_address'].get('zip_code')
    except AttributeError:
        print('could not parse customer {}, {}'.format(
            customer.customer_id, customer_info))
    customer.save()
    return customer
