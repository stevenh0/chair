from django import template
from datetime import datetime

register = template.Library()


@register.filter
def date_formater(date_tz, include_how_long_ago=False):
    if (include_how_long_ago):
        return datetime.strptime(date_tz, "%Y-%m-%dT%H:%M:%SZ")
    else:
        return datetime.strptime(date_tz, "%Y-%m-%dT%H:%M:%SZ")
