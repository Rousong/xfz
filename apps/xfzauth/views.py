from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.cache import cache
from .forms import LoginForm, RegisterForm
from utils import restful
from utils.captcha.xfzcaptcha import Captcha
from utils.aliyunsdk import aliyunsms

User = get_user_model()


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message='你的账号已被冻结！')
        else:
            return restful.params_error(message='手机号或者密码错误！')
    else:
        return restful.params_error(message=form.get_errors())


@require_GET
def logout_view(request):
    logout(request)
    return redirect('index')


@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(
                telephone=telephone, username=username, password=password)
        login(request, user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


@require_GET
def img_captcha(request):
    text, image = Captcha.gene_code()
    # BytesIO相当于一个管道，用于存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    # 从BytesIO管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    cache.set(text.lower(), text.lower(), 300)
    # 测试时打印图形验证码使用
    print(f'图形验证码：{text.lower()}')
    return response


@require_GET
def sms_captcha(request):
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    aliyunsms.send_sms(telephone, code)
    cache.set(telephone, code.lower(), 300)
    # 测试时打印短信验证码使用
    print(f'短信验证码：{code.lower()}')
    return restful.ok()
