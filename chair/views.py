from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chair.secrets import BESTBUY_KEY
import json
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