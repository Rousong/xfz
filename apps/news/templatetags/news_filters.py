from datetime import datetime
from django import template
from django.utils.timezone import now, localtime

register = template.Library()


@register.filter
def time_since(value):
    if not isinstance(value, datetime):
        return value
    timestamp = (now()-value).total_seconds()
    if timestamp < 60:
        return '刚刚'
    elif timestamp < 3600:
        return f'{int(timestamp/60)}分钟前'
    elif timestamp < 86400:
        return f'{int(timestamp/3600)}小时前'
    elif timestamp < 2592000:
        return f'{int(timestamp/86400)}天前'
    else:
        return value.strftime('%Y/%m/%d %H:%M')


@register.filter
def time_format(value):
    return localtime(value).strftime("%Y/%m/%d %H:%M:%S")\
        if isinstance(value, datetime) else value
