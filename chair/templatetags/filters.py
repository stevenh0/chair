from django import template
from datetime import datetime

register = template.Library()


@register.filter
def date_formater(date_tz):
    try:
        datetime_object = datetime.strptime(date_tz, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError: 
        # Some dates are missing 'Z'
        datetime_object = datetime.strptime(date_tz, "%Y-%m-%dT%H:%M:%S")
    finally:
        return datetime_object.strftime("%Y-%m-%d %H:%M")
