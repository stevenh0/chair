from secrets import NEWEGG_AUTH, NEWEGG_KEY
import requests
import json
import datetime

SELLER_ID = 'AFG1'


# TODO: actual newegg request here
def newegg_ship(order):
    newegg_json = get_newegg_order(order)
    headers = {'Authorization': NEWEGG_AUTH, 'SecretKey': NEWEGG_KEY,
               'Content-Type': 'application/json', 'Accept': 'application/json'}
    r = requests.post('https://api.newegg.com/marketplace/can/datafeedmgmt/feeds/submitfeed?sellerid={}&requesttype=MultiChannel_Orer_DATA'.format(SELLER_ID),
                      headers=headers, data=json.dumps(newegg_json))
    try:
        feed_id = json.loads(r)['ResponseBody']['ResponseList'][0]['RequestId']
        order.newegg_feed = feed_id
        order.save()
    except:
        return {'error': 'shipping failed for order {}'.format(order.order_id)}
    return {'success': 'shipping succeeded for order {}'.format(order.order_id)}


# can have multiple objects in this data feed, should probably iterate through them
def get_newegg_tracking_id(newegg_feed):
    headers = {'Authorization': NEWEGG_AUTH, 'SecretKey': NEWEGG_KEY,
               'Content-Type': 'application/json', 'Accept': 'application/json'}
    r = requests.get('https://api.newegg.com/marketplace/can/datafeedmgmt/feeds/result/{}?sellerid={}'
                     .format(newegg_feed, SELLER_ID), headers=headers)
    try:
        results = json.loads(r.content)['NeweggEnvelope']['Message']['ProcessingReport']['Result']
        for res in results:
            if res.get('AdditionalInfo') and res['AdditionalInfo'].get('TrackingNumber'):
                return res['AdditionalInfo'].get('TrackingNumber')
    except:
        return 'error in parsing feed {}'.format(newegg_feed)


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

