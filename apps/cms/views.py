import os
from urllib.parse import urlencode
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST
from django.conf import settings
from django.core.paginator import Paginator
from django.utils.timezone import make_aware
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
import shortuuid
import qiniu
from news.models import NewsCategory, Banner, News
from news.serializers import BannerSerializer
from course.models import CourseCategory, Teacher
from xfzauth.decorators import xfz_superuser_required
from utils import restful
from .forms import (
        EditNewsCategory, WriteNewsForm, AddBannerForm, PubCourseForm)

User = get_user_model()


@require_GET
@staff_member_required(login_url='index')
def index(request):
    return render(request, 'cms/index.html')


@method_decorator(permission_required(
    perm='news.add_news', login_url='/cms/'), name='dispatch')
class WriteNewsView(View):
    def get(self, request):
        categories = NewsCategory.objects.filter(is_deleted=False)
        context = {'categories': categories}
        return render(request, 'cms/write_news.html', context)

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            category_pk = form.cleaned_data.get('category_pk')
            news.category = NewsCategory.objects.get(pk=category_pk)
            news.author = request.user
            news.save()
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_GET
def news_category(request):
    categories = NewsCategory.objects.filter(is_deleted=False)
    context = {'categories': categories}
    return render(request, 'cms/news_category.html', context)


@require_POST
@permission_required(perm='news.add_news_category', login_url='/cms/')
def add_news_category(request):
    name = request.POST.get('name')
    category_obj, new_create = NewsCategory.objects.get_or_create(name=name)
    if new_create:
        return restful.ok()
    else:
        if category_obj.is_deleted:
            category_obj.is_deleted = False
            category_obj.save()
            return restful.ok()
        else:
            return restful.params_error(message='该分类名已存在！')


@require_POST
@permission_required(perm='news.change_news_category', login_url='/cms/')
def edit_news_category(request):
    form = EditNewsCategory(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            category_name_obj = NewsCategory.objects.get(name=name)
        except NewsCategory.DoesNotExist:
            try:
                category_pk_obj = NewsCategory.objects.get(pk=pk)
            except NewsCategory.DoesNotExist:
                return restful.params_error(message='原分类不存在！')
            else:
                category_pk_obj.name = name
                category_pk_obj.is_deleted = False
                category_pk_obj.save()
                return restful.ok()
        else:
            if category_name_obj.pk == pk:
                if category_name_obj.is_deleted:
                    category_name_obj.is_deleted = False
                    category_name_obj.save()
                    return restful.ok()
                else:
                    return restful.params_error(message='新输入分类名与原分类名相同')
            else:
                return restful.params_error(message='该分类名已存在！')
    else:
        return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm='news.delete_news_category', login_url='/cms/')
def delete_news_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).update(is_deleted=True)
        return restful.ok()
    except Exception:
        return restful.params_error('该分类不存在')


def banners(request):
    return render(request, 'cms/banners.html')


def banner_list(request):
    banners = Banner.objects.filter(is_deleted=False)
    serializer = BannerSerializer(banners, many=True)
    return restful.ok(data=serializer.data)


@require_POST
def add_banner(request):
    count = Banner.objects.filter(is_deleted=False).count()
    if count >= 6:
        return restful.params_error(message='最多只能添加6张轮播图！')
    form = AddBannerForm(request.POST)
    if form.is_valid():
        banner = form.save()
        return restful.ok(data={'banner_pk': banner.pk})
    else:
        return restful.params_error(message=form.get_errors())


def delete_banner(request):
    banner_pk = request.POST.get('bannerpk')
    Banner.objects.filter(pk=banner_pk).update(is_deleted=True)
    return restful.ok()


def edit_banner(request):
    pk = request.POST.get('pk')
    try:
        banner = Banner.objects.get(pk=pk)
    except Banner.DoesNotExist:
        return restful.params_error(message='传入参数错误！')
    form = AddBannerForm(request.POST, instance=banner)
    if form.is_valid():
        banner.priority = form.cleaned_data.get('priority')
        banner.image_url = form.cleaned_data.get('image_url')
        banner.link_to = form.cleaned_data.get('link_to')
        banner.save()
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(
    perm='news.view_news', login_url='/cms/'), name='dispatch')
class NewsListView(View):
    def get(self, request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_pk = int(request.GET.get('category_pk') or 0)
        url_query = '&'+urlencode({
            'start': start or '',
            'end': end or '',
            'title': title or '',
            'category_pk': category_pk or '',
        })
        newses = News.objects.select_related('category', 'author').filter(
                is_deleted=False)
        if start or end:
            if start:
                start_date = make_aware(datetime.strptime(start, '%Y/%m/%d'))
            else:
                start_date = make_aware(datetime(year=2018, month=1, day=1))
            if end:
                end_date = make_aware(datetime.strptime(end, '%Y/%m/%d'))
            else:
                end_date = make_aware(datetime.today())
            newses = newses.filter(pub_time__range=(start_date, end_date))
        if title:
            newses = newses.filter(title__icontains=title)
        if category_pk != 0:
            newses = newses.filter(category=category_pk)
        paginator = Paginator(newses, 2)
        page_obj = paginator.page(page)
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context = {
            **pagination_data,
            'categories': NewsCategory.objects.filter(is_deleted=False),
            'newses': page_obj.object_list,
            'url_query': url_query,
            'start': start,
            'end': end,
            'title': title,
            'category_pk': category_pk,
        }
        return render(request, 'cms/news_list.html', context)

    def get_pagination_data(self, paginator, page_obj, arount_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages
        left_pages = range(max(1, current_page-arount_count), current_page)
        right_pages = range(current_page+1,
                            min(num_pages+1, current_page+arount_count+1))
        return {
            'current_page': current_page,
            'num_pages': num_pages,
            'left_pages': left_pages,
            'right_pages': right_pages,
        }


@method_decorator(permission_required(
    perm='news.change_news', login_url='/cms/'), name='dispatch')
class EditNewsView(View):
    def get(self, request):
        news_pk = request.GET.get('news_pk')
        news = News.objects.get(pk=news_pk, is_deleted=False)
        context = {
            'news': news,
            'categories': NewsCategory.objects.filter(is_deleted=False),
        }
        return render(request, 'cms/write_news.html', context)

    def post(self, request):
        news_pk = request.POST.get('news_pk')
        news = News.objects.get(pk=news_pk, is_deleted=False)
        form = WriteNewsForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            category_pk = int(form.cleaned_data.get('category_pk'))
            if news.category_id != category_pk and NewsCategory.objects.filter(
                    pk=category_pk, is_deleted=False).exists():
                news.category_id = category_pk
            news.author = request.user
            news.save()
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm='news.delete_news', login_url='/cms/')
def delete_news(request):
    news_pk = request.POST.get("news_pk")
    News.objects.filter(pk=news_pk).update(is_deleted=True)
    return restful.ok()


@require_POST
@staff_member_required(login_url='/cms/')
def upload_file(request):
    file = request.FILES.get('file')
    old_name = file.name
    pos = old_name.rfind('.')
    if pos != -1:
        new_name = old_name[:pos]+shortuuid.uuid()+old_name[pos:]
    else:
        new_name = old_name+shortuuid.uuid()
    with open(os.path.join(settings.MEDIA_ROOT, new_name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    file_url = request.build_absolute_uri(settings.MEDIA_URL+new_name)
    return restful.ok(data={'url': file_url})


@require_GET
@staff_member_required(login_url='/cms/')
def qntoken(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    bucket = settings.QINIU_BUCKET_NAME
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket)
    return restful.ok(data={"token": token})


class PubCourse(View):
    def get(self, request):
        context = {
            'categories': CourseCategory.objects.filter(is_deleted=False),
            'teachers': Teacher.objects.filter(is_deleted=False),
        }
        return render(request, 'cms/pub_course.html', context)

    def post(self, request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            category_pk = form.cleaned_data.get('category_pk')
            course.category = CourseCategory.objects.get(pk=category_pk)
            teacher_pk = form.cleaned_data.get('teacher_pk')
            course.teacher = Teacher.objects.get(pk=teacher_pk)
            course.save()
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@xfz_superuser_required
def staffs_view(request):
    staffs = User.objects.filter(is_active=True, is_staff=True)
    context = {'staffs': staffs}
    return render(request, 'cms/staffs.html', context)


@method_decorator(xfz_superuser_required, name='dispatch')
class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {'groups': groups}
        return render(request, 'cms/add_staff.html', context)

    def post(self, request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone, is_active=True).first()
        if user:
            user.is_staff = True
            group_ids = request.POST.getlist('groups')
            groups = Group.objects.filter(pk__in=group_ids)
            user.groups.set(groups)
            user.save()
            return redirect('cms:staffs')
        else:
            messages.info(request, '手机号码不存在')
            return redirect('cms:add_staff')
