from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500


def _result(code=HttpCode.ok, message='', data=None, **kwargs):
    json_dict = {**kwargs, 'code': code, 'message': message, 'data': data}
    return JsonResponse(json_dict)


def ok(message='', data=None):
    return _result(message=message, data=data)


def params_error(message='',  data=None):
    return _result(code=HttpCode.paramserror, message=message, data=data)


def unauth(message='',  data=None):
    return _result(code=HttpCode.unauth, message=message, data=data)


def method_error(message='',  data=None):
    return _result(code=HttpCode.methoderror, message=message, data=data)


def server_error(message='',  data=None):
    return _result(code=HttpCode.servererror, message=message, data=data)
