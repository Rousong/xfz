from django.urls import path
from .views import login_view, logout_view, img_captcha, sms_captcha, register

app_name = 'xfzauth'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('img_captcha/', img_captcha, name='img_captcha'),
    path('sms_captcha/', sms_captcha, name='sms_captcha'),
]
