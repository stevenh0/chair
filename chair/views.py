from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from secrets import BESTBUY_KEY, CARRIER_CODE
import requests
import json
from chair.models import Order, Customer
from chair.product_info import PRODUCT_INFO
import datetime


# workflow: load bestbuy orders from last date, grab unshipped orders, display.
# have option to fulfill order - user clicks fulfill = send newegg shipment, update
# bestbuy order status
@login_required()
def console(request):
    return render(request, "console.html", context={"order_info": Order.objects.all()[:10]})


@login_required()
def newegg_fulfill(request, order_id):
    order = Order.objects.filter(order_id=order_id)
    for o in order:
        newegg_order = get_newegg_order(o)
        newegg_ship(newegg_order)


# TODO: actual newegg request here
def newegg_ship(newegg_json):
    pass


def get_bestbuy_order():
    headers = {'Authorization': BESTBUY_KEY}
    r = requests.get('https://marketplace.bestbuy.ca/api/orders', headers=headers)
    # grab necessary info and return it, probably some customer information stuff
    order_info = []
    customer_info = []
    return order_info, customer_info


# TODO: multiple objects in a single order - what format
# TODO: what is SalesChannel
def get_newegg_order(order):
    customer = order.customer_id
    today = datetime.date.today().strftime('%m/%d/%Y')
    channel = "PulseLabz"
    shipping = "CAN Ground(2-7 Business Days)"
    newegg = {
        "-xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "Header": { "DocumentVersion": "1.0" },
        "MessageType": "MultiChannelOrderCreation",
        "Message": {
            "MultiChannelOrder": {
                "Order": {
                    "OrderDate": today,
                    "SalesChannel": channel,
                    "SellerOrderID": order.order_id,
                    "ShippingMethod": shipping,
                    "ShipToFirstName": customer.firstname,
                    "ShipToLastName": customer.lastname,
                    "ShipToAddressLine1": customer.street,
                    "ShipToCity": customer.city,
                    "ShipToState": customer.state,
                    "ShipToPostalCode": customer.zip,
                    "ShipToCountry": customer.country,
                    "ShipToPhoneNumber": customer.phone,
                    "ItemList": {
                        "Item": {"SellerPartNumber": order.part_number,
                                 "Quantity": order.quantity}
                    }
                }
            }
        }
    }
    return newegg


def update_tracking(order_id, tracking_number):
    headers = {'Authorization': BESTBUY_KEY}
    tracking_data = {'carrier_code': CARRIER_CODE, 'tracking_number': tracking_number}
    requests.put('https://marketplace.bestbuy.ca/api/orders/{}/accept'.format(order_id),
                 data=json.dumps(tracking_data), headers=headers)
    return 1


# date should be in format yyyy-MM-dd
def grab_orders(date=None):
    headers = {'Authorization': BESTBUY_KEY}
    r = requests.get('https://marketplace.bestbuy.ca/api/orders', {"start_date": date, "paginate": False}, headers=headers)
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
        order, created = Order.objects.get_or_create(order_id=order_info.get('order_id'), product_name=product_name)
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


# TODO: what do condo addresses look like
def update_customer_info(customer_info):
    customer, created = Customer.objects.get_or_create(customer_id=customer_info.get('customer_id'))
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
        print('could not parse customer {}, {}'.format(customer.customer_id, customer_info))
    customer.save()
    return customer
