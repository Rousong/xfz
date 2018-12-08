from functools import wraps
from django.shortcuts import redirect
from django.http import Http404
from utils import restful


def xfz_login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth('请先登录！')
            else:
                return redirect('index')
    return wrapper


def xfz_superuser_required(viewfunc):
    @wraps(viewfunc)
    def decorator(request, *args, **kwargs):
        if request.user.is_superuser:
            return viewfunc(request, *args, **kwargs)
        else:
            raise Http404()
    return decorator
