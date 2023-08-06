import json
import time
import functools

import bizerror
from .response import HttpResponse

def json_api(func):
    """Json api handler decorater.
    
    Example:

    @json_api
    def ping(http_request, http_response):
        return {
            "success": True,
            "result": "pong",
            "error": {
                "code": 0,
                "message": "OK",
            }
        }

    The response data:

    {
        "success": True,
        "result": "pong",
        "error": {
            "code": 0,
            "message": "OK",
        }
    }
    """
    def wrapper(http_request, http_response):
        result = func(http_request, http_response)
        if isinstance(result, HttpResponse):
            return
        http_response.content_type = "application/json"
        http_response.content = json.dumps(result, ensure_ascii=False).encode("utf-8")
    return functools.wraps(func)(wrapper)

def jsonp_api(callback_field="callback"):
    """Jsonp api handler decorater.

    Example:

    @jsonp_api()
    def ping(http_request, http_response):
        return "pong"

    """
    def wrapper_outer(func):
        def wrapper(http_request, http_response):
            result = func(http_request, http_response)
            if isinstance(result, HttpResponse):
                return
            callback = http_request.GET.get(callback_field, "callback")
            http_response.content_type = "application/javascript"
            http_response.content = "{callback}({data});".format(callback=callback, data=json.dumps(result, ensure_ascii=False))
        return functools.wraps(func)(wrapper)
    return wrapper_outer

def simplejson_api(func):
    """Json api handler with result packer decorater.

    Example:

    @json_api
    def ping(http_request, http_response):
        return "pong"

    The response data:

    {
        "success": True,
        "result": "pong",
        "error": {
            "code": 0,
            "message": "OK",
        }
    }

    """
    def wrapper(http_request, http_response):
        try:
            result = func(http_request, http_response)
            if isinstance(result, HttpResponse):
                return
            result = {
                "success": True,
                "result": result,
                "error": {
                    "code": 0,
                    "message": "OK",
                }
            }
        except Exception as error:
            error = bizerror.BizError(error)
            result = {
                "success": False,
                "result": None,
                "error": {
                    "code": error.code,
                    "message": error.message,
                }
            }
        http_response.content_type = "application/json"
        http_response.content = json.dumps(result, ensure_ascii=False).encode("utf-8")
    return functools.wraps(func)(wrapper)

def simplejsonp_api(callback_field="callback"):
    """Jsonp api handler with result packer decorater.
    """
    def wrapper_outer(func):
        def wrapper(http_request, http_response):
            try:
                result = func(http_request, http_response)
                if isinstance(result, HttpResponse):
                    return
                result = {
                    "success": True,
                    "result": result,
                    "error": {
                        "code": 0,
                        "message": "OK",
                    }
                }
            except Exception as error:
                error = bizerror.BizError(error)
                result = {
                    "success": False,
                    "result": None,
                    "error": {
                        "code": error.code,
                        "message": error.message,
                    }
                }
            callback = http_request.GET.get(callback_field, "callback")
            http_response.content_type = "application/javascript"
            http_response.content = "{callback}({data});".format(callback=callback, data=json.dumps(result, ensure_ascii=False))
        return functools.wraps(func)(wrapper)
    return wrapper_outer
