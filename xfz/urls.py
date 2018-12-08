from django.urls import path, include
from news.views import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('news/', include('news.urls', namespace='news')),
    path('cms/', include('cms.urls', namespace='cms')),
    path('account/', include('xfzauth.urls', namespace='xfzauth')),
    path('course/', include('course.urls', namespace='course')),
    path('payinfo/', include('payinfo.urls', namespace='payinfo')),
    path('ueditor/', include('ueditor.urls', namespace='ueditor')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# django-debug-toolbar配置
if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
