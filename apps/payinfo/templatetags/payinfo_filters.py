from django import template
from payinfo.models import PayinfoOrder

register = template.Library()


@register.filter
def is_buyed(payinfo, user):
    if user.is_authenticated:
        return PayinfoOrder.objects.filter(
                payinfo=payinfo, buyer=user, status=2, is_deleted=False
                ).exists()
    else:
        return False
