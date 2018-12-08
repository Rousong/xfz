import os
import time
import hmac
from hashlib import sha256, md5
from django.shortcuts import render, reverse
from django.http import Http404
from django.conf import settings
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from utils import restful
from xfzauth.decorators import xfz_login_required
from .models import Course, CourseOrder


@require_GET
def course_index(request):
    context = {
        'courses': Course.objects.select_related('teacher').filter(
            is_deleted=False),
    }
    return render(request, 'course/course_index.html', context)


@require_GET
def course_detail(request, course_id):
    try:
        course = Course.objects.select_related('teacher').get(
                pk=course_id, is_deleted=False)
    except Course.DoesNotExist:
        raise Http404
    if request.user.is_authenticated:
        has_buy = CourseOrder.objects.filter(
                course=course, buyer=request.user, status=2, is_deleted=False
                ).exists()
    else:
        has_buy = False
    context = {'course': course, 'has_buy': has_buy}
    return render(request, 'course/course_detail.html', context)


@require_GET
@xfz_login_required
def course_token(request):
    course_id = request.GET.get('course_id')
    has_buy = CourseOrder.objects.filter(
            course_id=course_id, buyer=request.user, status=2, is_deleted=False
            ).exists()
    if has_buy:
        video_file = request.GET.get('video_url')
        expiration_time = int(time.time())+7200
        USER_ID = settings.BAIDU_CLOUD_USER_ID
        USER_KEY = settings.BAIDU_CLOUD_USER_KEY
        extension = os.path.splitext(video_file)[1]
        media_id = video_file.split('/')[-1].replace(extension, '')
        key = USER_KEY.encode('utf-8')
        message = (f'/{media_id}/{expiration_time}').encode('utf-8')
        signature = hmac.new(key, message, digestmod=sha256).hexdigest()
        token = f'{signature}_{USER_ID}_{expiration_time}'
        return restful.ok(data={'token': token})
    else:
        return restful.unauth(message="请先购买课程")


@require_GET
@xfz_login_required
def course_order(request, course_pk):
    course = Course.objects.get(pk=course_pk, is_deleted=False)
    order = CourseOrder.objects.create(
            course=course, buyer=request.user, amount=course.price)
    notify_url = request.build_absolute_uri(reverse('course:notify_view'))
    return_url = request.build_absolute_uri(
            reverse('course:course_detail', kwargs={'course_id': course.pk}))
    context = {
        'goods': course,
        'order': order,
        'notify_url': notify_url,
        'return_url': return_url,
    }
    return render(request, 'course/course_order.html', context)


@xfz_login_required
@require_POST
def course_order_key(request):
    goodsname = request.POST.get('goodsname')
    istype = request.POST.get('istype')
    notify_url = request.POST.get('notify_url')
    orderid = request.POST.get('orderid')
    price = request.POST.get('price')
    return_url = request.POST.get('return_url')
    token = '71a52d120b58b08f8812d5f6bf4b7c1c'
    uid = '64716d1aa3b93a46dc53197d'
    orderuid = str(request.user.pk)
    key = md5((
        goodsname+istype+notify_url+orderid+orderuid+price+return_url+token+uid
        ).encode('utf-8')).hexdigest()
    return restful.ok(data={'key': key})


@csrf_exempt
@require_POST
@xfz_login_required
def notify_view(request):
    orderid = request.POST.get('orderid')
    CourseOrder.objects.filter(pk=orderid, is_deleted=False).update(status=2)
    return restful.ok()
