from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from secrets import BESTBUY_KEY, CARRIER_CODE
import requests
import json
from chair.models import Order, Customer
import datetime


@login_required()
def console(request):
	order_info, customer_info = get_bestbuy_orders()
	if AUTO_FULFILL:
		newegg_order = create_newegg_order(customer_info)
		fulfill_newegg_order(newegg_order)
	return render(request, "console.html", context={"order_info": order_info, "customer_info": customer_info})


@login_required():
def newegg_fulfill(request):
	newegg_order = create_newegg_order(customer_info)
	fulfill_newegg_order(newegg_order)



def get_bestbuy_order():
	headers = { 'Authorization': BESTBUY_KEY}
	r = requests.get('https://marketplace.bestbuy.ca/api/orders', headers=headers)
	# grab necessary info and return it, probably some customer information stuff
	order_info = []
	customer_info = []
	return order_info, customer_info


# TODO: multiple objects in a single order - what format
# TODO: what is SalesChannel
def get_newegg_order(orders, customer):
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
	        "SellerOrderID": order.id,
	        "ShippingMethod": shipping,
	        "ShipToFirstName": customer.first_name,
	        "ShipToLastName": customer.last_name,
	        "ShipToAddressLine1": customer.address,
	        "ShipToCity": customer.city,
	        "ShipToState": customer.state,
	        "ShipToPostalCode": customer.postal_code,
	        "ShipToCountry": customer.county,
	        "ShipToPhoneNumber": customer.phone,
	        "ItemList": {
	          "Item": [{
	              "SellerPartNumber": order.part_number,
	              "Quantity": order.quantity
	            } for order in orders]
	        }
	      }
	    }
	  }
	}
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
