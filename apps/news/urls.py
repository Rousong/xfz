from django.urls import path, include
from .views import news_detail, news_list, public_comment

app_name = 'news'
urlpatterns = [
    path('search/', include('haystack.urls')),
    path('<int:news_pk>/', news_detail, name='news_detail'),
    path('list/', news_list, name='news_list'),
    path('public_comment/', public_comment, name='public_comment'),
]
