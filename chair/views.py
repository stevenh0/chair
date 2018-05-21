from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse

from secrets import BESTBUY_KEY, CARRIER_CODE
from chair.models import Order, OrderStatus
from chair.order_processing.bestbuy import grab_orders
from chair.order_processing.newegg import get_newegg_tracking_id, newegg_ship

import requests
import json
import datetime


# workflow: load bestbuy orders from last date, grab unshipped orders, display.
# have option to fulfill order - user clicks fulfill = send newegg shipment -> returns newegg_feed
# have to parse newegg_feed to get tracking_id -> update tracking_id on bestbuy side
@login_required()
def dashboard(request):
    return render(request, "chair/dashboard.html", context={"order_info": Order.objects.all()[:10]})


@login_required()
def grab_latest_orders(request):
    settings = OrderStatus.objects.first()
    date = settings.last_update
    grab_orders(date)
    settings.last_update = datetime.date.today().strftime('%Y/%m/%d')
    settings.save()


@login_required()
def newegg_fulfill(request, order_id):
    order = Order.objects.filter(order_id=order_id)
    for o in order:
        newegg_ship(o)
    return redirect(reverse('dashboard'))


# update tracking information for an order - can't call this before shipping the order via newegg
# and parsing the tracking_id from the newegg feed
@login_required()
def update_tracking(request, order_id):
    order = Order.objects.get(order_id=order_id)
    tracking_id = get_newegg_tracking_id(order.newegg_feed)
    if not 'error' in tracking_id:
        return JsonResponse({'status': 'error', 'message': 'tracking number has not been updated yet for this order'})
    headers = {'Authorization': BESTBUY_KEY}
    tracking_data = {'carrier_code': CARRIER_CODE,
                     'tracking_number': tracking_id}
    requests.put('https://marketplace.bestbuy.ca/api/orders/{}/accept'.format(order_id),
                 data=json.dumps(tracking_data), headers=headers)
    order.tracking_id = tracking_id
    order.save()
    return JsonResponse({'status': 'success', 'message': 'tracking number for order {} has been updated'.format(order_id)})
