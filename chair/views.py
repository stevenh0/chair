from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from secrets import BESTBUY_KEY
import requests
import json


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
    tracking_data = {'carrier_code': 'CPCL', 'tracking_number': tracking_number}
    requests.put('https://marketplace.bestbuy.ca/api/orders/{}/accept'.format(order_id),
                 data=json.dumps(tracking_data), headers=headers)
    return 1


# date should be in format yyyy-MM-dd
def grab_orders(date):
    headers = {'Authorization': BESTBUY_KEY}
    r = requests.get('https://marketplace.bestbuy.ca/api/orders', {"start_date": ""}, headers=headers)
    r_data = json.loads(r)
    orders = r_data.get('orders')
    for order in orders:
        # grab necessary fields for newegg stuff and enter them into the db
        pass
    return len(orders)
