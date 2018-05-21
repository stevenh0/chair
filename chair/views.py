from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

from scraper.settings import BESTBUY_KEY, CARRIER_CODE
from chair.models import Order, OrderStatus
from chair.order_processing.bestbuy import grab_orders, process_order
from chair.order_processing.newegg import get_newegg_tracking_id, newegg_ship

import requests
import json
import datetime


# workflow: load bestbuy orders from last date, grab unshipped orders, display.
# have option to fulfill order - user clicks fulfill = send newegg shipment -> returns newegg_feed
# have to parse newegg_feed to get tracking_id -> update tracking_id on bestbuy side
@login_required()
def dashboard(request):
    completed = Order.objects.filter(
        Q(status='RECEIVED') | Q(status='CANCELLED') | Q(status='REFUSED') | Q(status='CLOSED'))
    pending = Order.objects.filter(
        Q(status='WAITING_ACCEPTANCE') | Q(status='WAITING_DEBIT_PAYMENT') | Q(status='SHIPPING'))
    return render(request, "chair/dashboard.html", context={'completed': reversed(completed), 'pending': reversed(pending), 'completed_len': len(completed), 'pending_len': len(pending)})


@login_required()
def grab_latest_orders(request):
    settings = OrderStatus.objects.first()
    date = (datetime.date.today() - datetime.timedelta(weeks=4)).strftime('%Y-%m-%d')
    updated = grab_orders(date)
    settings.last_update = datetime.date.today().strftime('%Y-%m-%d')
    settings.save()
    if updated > 0:
        return JsonResponse({'status': 'success', 'message': 'orders have been updated'})
    return JsonResponse({'status': 'failure', 'message': 'no new orders'})


@login_required()
def newegg_fulfill(request, order_id):
    order = Order.objects.filter(order_id=order_id)
    for o in order:
        newegg_ship(o)
        return JsonResponse(
            {'status': 'success', 'message': 'shipment for order {} has been created'.format(order_id)})


@login_required()
def accept_order(request, order_id):
    r = process_order(order_id, True)
    if not r.status_code == 204:
        return JsonResponse({'status': 'error', 'message': 'error in accepting order {}'.format(order_id)})
    # sync db with orders
    date = (datetime.date.today() - datetime.timedelta(weeks=4)).strftime('%Y-%m-%d')
    grab_orders(date)
    return JsonResponse({'status': 'success', 'message': 'order {} has been accepted'.format(order_id)})


@login_required()
def reject_order(request, order_id):
    r = process_order(order_id, False)
    if not r.status_code == 204:
        return JsonResponse({'status': 'error', 'message': 'error in accepting order {}'.format(order_id)})
    date = (datetime.date.today() - datetime.timedelta(weeks=4)).strftime('%Y-%m-%d')
    # sync db with orders
    grab_orders(date)
    return JsonResponse({'status': 'success', 'message': 'order {} has been rejected'.format(order_id)})


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
