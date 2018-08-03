from django import template
from datetime import datetime

register = template.Library()


@register.filter
def date_formater(date_tz, include_how_long_ago=False):
    try:
        return datetime.strptime(date_tz, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return datetime.strptime(date_tz, "%Y-%m-%dT%H:%M:%S")
