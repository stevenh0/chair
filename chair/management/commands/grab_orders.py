from django.core.management.base import BaseCommand
from chair.order_processing.bestbuy import grab_orders


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        grab_orders()
