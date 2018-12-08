from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from xfzauth.decorators import xfz_login_required
from utils import restful
from .models import News, NewsCategory, Comment, Banner
from .serializers import NewsSerializer, CommentSerializer
from .forms import PublicCommentForm


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category', 'author').filter(
            is_deleted=False)[0:count]
    categories = NewsCategory.objects.filter(is_deleted=False)
    context = {
        'newses': newses,
        'categories': categories,
        'banners': Banner.objects.filter(is_deleted=False),
    }
    return render(request, 'news/index.html', context)


def news_list(request):
    page = int(request.GET.get('p', 1))
    category_pk = int(request.GET.get('category_pk', 0))
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start+settings.ONE_PAGE_NEWS_COUNT
    if category_pk == 0:
        newses = News.objects.select_related('category', 'author').filter(
                is_deleted=False)[start:end]
    else:
        newses = News.objects.select_related('category', 'author').filter(
                is_deleted=False, category__pk=category_pk)[start:end]
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.ok(data=data)


def news_detail(request, news_pk):
    try:
        news = News.objects.select_related('category', 'author').get(
                pk=news_pk, is_deleted=False)
    except News.DoesNotExist:
        raise Http404
    comments = news.comments.select_related('author').filter(is_deleted=False)
    context = {'news': news, 'comments': comments}
    return render(request, 'news/news_detail.html', context)


@require_POST
@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_pk = form.cleaned_data.get('news_pk')
        content = form.cleaned_data.get('content')
        try:
            news = News.objects.get(pk=news_pk, is_deleted=False)
        except News.DoesNotExist:
            raise Http404
        comment = Comment.objects.create(content=content, news=news,
                                         author=request.user)
        serializer = CommentSerializer(comment)
        return restful.ok(data=serializer.data)
    else:
        return restful.params_error(message=form.get_errors())


def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context['newses'] = newses
    return render(request, 'search/search1.html', context)
