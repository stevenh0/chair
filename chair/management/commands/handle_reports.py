from django.core.management.base import BaseCommand
from chair.order_processing.newegg import parse_report
from chair.models import Report


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        reports = Report.objects.filter(processed=0)
        for report in reports:
            parse_report(report.report_id)
