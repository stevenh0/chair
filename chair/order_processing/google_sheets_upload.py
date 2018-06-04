import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from chair.models import Order


def post_order_info(order_id):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('pulselabz.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1kQHu41vQ6QL1_5k-hbtPi20AI6YOKfx0lcBTlDtshD8/edit?ts=5b1455d8#gid=1703849860')
    worksheet = sheet.get_worksheet(0)
    next_free = len(worksheet.col_values(2)) + 1
    order = Order.objects.get(order_id=order_id)
    today = datetime.datetime.today().strftime('%B %d')
    worksheet.update_acell('B{}'.format(next_free), today)
    worksheet.update_acell('D{}'.format(next_free), order.part_number)
    worksheet.update_acell('E{}'.format(next_free), order.total_price)
    worksheet.update_acell('F{}'.format(next_free), order.customer_id.state)
    worksheet.update_acell('O{}'.format(next_free), order.bestbuy_commission)
    worksheet.update_acell('Q{}'.format(next_free), 'Ground-Newegg')
    worksheet.update_acell('T{}'.format(next_free), order.tracking_id)
    worksheet.update_acell('Y{}'.format(next_free), order.customer_id.firstname)
    worksheet.update_acell('Z{}'.format(next_free), order.customer_id.lastname)
    worksheet.update_acell('AA{}'.format(next_free), order.customer_id.phone)
    worksheet.update_acell('AB{}'.format(next_free), order.customer_id.street)
    worksheet.update_acell('AC{}'.format(next_free), order.customer_id.zip)
    worksheet.update_acell('AD{}'.format(next_free), order.customer_id.city)
    worksheet.update_acell('AE{}'.format(next_free), order.customer_id.state)