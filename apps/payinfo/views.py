import os
from django.shortcuts import render, reverse
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from xfzauth.decorators import xfz_login_required
from utils import restful
from .models import Payinfo, PayinfoOrder


def index(request):
    payinfos = Payinfo.objects.filter(is_deleted=False)
    context = {'payinfos': payinfos}
    return render(request, 'payinfo/payinfo.html', context)


@xfz_login_required
def payinfo_order(request):
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    order = PayinfoOrder.objects.create(payinfo=payinfo, buyer=request.user,
                                        amount=payinfo.price)
    notify_url = request.build_absolute_uri(reverse('payinfo:notify_view'))
    return_url = request.build_absolute_uri(reverse('payinfo:index'))
    context = {
        'goods': payinfo,
        'order': order,
        'notify_url': notify_url,
        'return_url': return_url,
    }
    return render(request, 'course/course_order.html', context)


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    PayinfoOrder.objects.filter(pk=orderid, is_deleted=False).update(status=2)
    return restful.ok()


@xfz_login_required
def download(request):
    payinfo_id = request.GET.get('payinfo_id')
    order = PayinfoOrder.objects.filter(
            payinfo_id=payinfo_id, buyer=request.user, status=2,
            is_deleted=False).first()
    if order:
        path = order.payinfo.path
        fp = open(os.path.join(settings.MEDIA_ROOT, path), 'rb')
        response = FileResponse(fp)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] =\
            f'attachment;filename={path.split("/")[-1]}'
        return response
    else:
        return Http404
