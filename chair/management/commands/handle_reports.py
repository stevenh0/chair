from django.core.management.base import BaseCommand
from chair.order_processing.newegg import parse_report, get_report
from chair.models import Report, Order


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        reports = Report.objects.filter(processed=0)
        for report in reports:
            parse_report(report.request_id)
        if Order.objects.filter(newegg_shipped=True, has_report=False).count() > 0:
            get_report()
