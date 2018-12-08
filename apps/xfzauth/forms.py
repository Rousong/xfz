from django import forms
from django.core import validators
from django.core.cache import cache
from apps.forms import FormMixin
from .models import User


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(
            max_length=11, min_length=11,
            error_messages={
                'max_length': '手机号不能超过11位数字！',
                'min_length': '手机号不能少于11位数字！',
                'required': '请输入手机号！',
            },
            validators=[
                validators.RegexValidator(
                    r'1[3-9]\d{9}', message='请输入正确格式的手机号')
            ]
    )
    password = forms.CharField(
            max_length=20, min_length=6,
            error_messages={
                'max_length': '密码不能超过20位字符！',
                'min_length': '密码不能少于6位字符！',
                'required': '请输入密码！',
            }
    )
    remember = forms.BooleanField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(
            max_length=11, min_length=11,
            error_messages={
                'max_length': '手机号不能超过11位数字！',
                'min_length': '手机号不能少于11位数字！',
                'required': '请输入手机号！',
            },
            validators=[
                validators.RegexValidator(
                    r'1[3-9]\d{9}', message='请输入正确格式的手机号')
            ]
    )
    username = forms.CharField(
            max_length=30, min_length=4,
            error_messages={
                'max_length': '用户名不能超过30位字符！',
                'min_length': '用户名不能少于4位字符！',
                'required': '请输入用户名！',
            }
    )
    password1 = forms.CharField(
            max_length=20, min_length=6,
            error_messages={
                'max_length': '密码不能超过20位字符！',
                'min_length': '密码不能少于6位字符！',
                'required': '请输入密码！',
            }
    )
    password2 = forms.CharField(
            max_length=20, min_length=6,
            error_messages={
                'max_length': '确认密码不能超过20位字符！',
                'min_length': '确认密码不能少于6位字符！',
                'required': '请输入确认密码！',
            }
    )
    img_captcha = forms.CharField(
            max_length=4, min_length=4,
            error_messages={
                'max_length': '请输入4位图形验证码',
                'min_length': '请输入4位图形验证码',
                'required': '请输入4位图形验证码',
            },
            validators=[
                validators.RegexValidator(
                    r'[a-zA-Z0-9]{4}', message='请输入正确的图形验证码！')
            ]
    )
    sms_captcha = forms.CharField(
            max_length=4, min_length=4,
            error_messages={
                'max_length': '请输入4位短信验证码',
                'min_length': '请输入4位短信验证码',
                'required': '请输入4位短信验证码',
            },
            validators=[
                validators.RegexValidator(
                    r'[a-zA-Z0-9]{4}', message='请输入正确的短信验证码！')
            ]
    )

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if not (password1 and password2) or password1 != password2:
            raise forms.ValidationError('密码输入错误！')

        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha)
        if not (img_captcha and cached_img_captcha)\
                or cached_img_captcha != img_captcha.lower():
            raise forms.ValidationError('图形验证码错误！')

        telephone = cleaned_data.get('telephone')
        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)
        if not (sms_captcha and cached_sms_captcha)\
                or cached_sms_captcha != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误！')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('该手机号已注册！')
