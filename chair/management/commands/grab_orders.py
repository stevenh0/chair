from django.core.management.base import BaseCommand
from chair.order_processing.bestbuy import grab_orders, process_order
from chair.models import Order


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        grab_orders()
        for order in Order.objects.filter(status='WAITING_ACCEPTANCE'):
            process_order(order.order_id, True)
