from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from secrets import BESTBUY_KEY, CARRIER_CODE
import requests
import json
from chair.models import Order, Customer


@login_required()
def console(request):
    return render(request, "console.html", context={"secret": 'lol'})


def process_order(order_id, accept):
    headers = {'Authorization': BESTBUY_KEY}
    acceptance_data = {'order_lines': [{'accepted': accept, 'id': order_id}]}
    requests.put('https://marketplace.bestbuy.ca/api/orders/{}/accept'.format(order_id),
                 data=json.dumps(acceptance_data), headers=headers)
    return 1


def update_tracking(order_id, tracking_number):
    headers = {'Authorization': BESTBUY_KEY}
    tracking_data = {'carrier_code': CARRIER_CODE, 'tracking_number': tracking_number}
    requests.put('https://marketplace.bestbuy.ca/api/orders/{}/accept'.format(order_id),
                 data=json.dumps(tracking_data), headers=headers)
    return 1


# date should be in format yyyy-MM-dd
def grab_orders(date):
    headers = {'Authorization': BESTBUY_KEY}
    r = requests.get('https://marketplace.bestbuy.ca/api/orders', {"start_date": date}, headers=headers)
    r_data = json.loads(r)
    orders = r_data.get('orders')
    for order in orders:
        # grab necessary fields for newegg stuff and enter them into the db
        load_order(order)
        pass
    return len(orders)

# TODO: how does newegg know what product to ship
# fill in information needed for an order
def load_order(order_info):
    order, created = Order.objects.get_or_create(order_id=order_info.get('order_id'))
    customer = update_customer_info(order_info.get('customer'))
    order.customer = customer
    status = order_info.get('order_state')


# TODO: do we need billing address? assuming no
# TODO: what do condo addresses look like
def update_customer_info(customer_info):
    customer, created = Customer.objects.get_or_create(customer_id=customer_info.get('customer_id'))
    customer.firstname = customer_info.get('firstname')
    customer.lastname = customer_info.get('lastname')
    customer.country = customer_info['shipping_adress'].get('country')
    customer.city = customer_info['shipping_adress'].get('city')
    customer.phone = customer_info['shipping_adress'].get('phone')
    customer.state = customer_info['shipping_adress'].get('state')
    customer.street = customer_info['shipping_adress'].get('street_1')
    customer.zip = customer_info['shipping_adress'].get('zip_code')
    customer.save()
    return customer
