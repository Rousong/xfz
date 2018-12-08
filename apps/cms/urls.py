from django.urls import path
from .views import (
        index, WriteNewsView, news_category, add_news_category,
        edit_news_category, delete_news_category, upload_file, qntoken,
        banners, add_banner, banner_list, delete_banner, edit_banner,
        NewsListView, EditNewsView, delete_news, PubCourse, staffs_view,
        AddStaffView)

app_name = 'cms'
urlpatterns = [
    path('', index, name='index'),
    path('write_news/', WriteNewsView.as_view(), name='write_news'),
    path('edit_news/', EditNewsView.as_view(), name='edit_news'),
    path('delete_news/', delete_news, name='delete_news'),
    path('news_list/', NewsListView.as_view(), name='news_list'),
    path('news_category/', news_category, name='news_category'),
    path('add_news_category/', add_news_category, name='add_news_category'),
    path('edit_news_category/', edit_news_category, name='edit_news_category'),
    path('delete_news_category/', delete_news_category,
         name='delete_news_category'),
    path('banners/', banners, name='banners'),
    path('add_banner/', add_banner, name='add_banner'),
    path('delete_banner/', delete_banner, name='delete_banner'),
    path('edit_banner/', edit_banner, name='edit_banner'),
    path('banner_list/', banner_list, name='banner_list'),
    path('upload_file/', upload_file, name='upload_file'),
    path('qntoken/', qntoken, name='qntoken'),
    path('pub_course/', PubCourse.as_view(), name='pub_course'),
    path('staffs/', staffs_view, name='staffs'),
    path('add_staff/', AddStaffView.as_view(), name='add_staff'),
]
