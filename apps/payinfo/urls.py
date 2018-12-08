from django.urls import path
from .views import index, payinfo_order, notify_view, download

app_name = 'payinfo'
urlpatterns = [
    path('', index, name='index'),
    path('payinfo_order/', payinfo_order, name='payinfo_order'),
    path('notify_url/', notify_view, name='notify_view'),
    path('download/', download, name='download'),
]
