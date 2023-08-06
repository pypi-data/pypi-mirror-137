
from functools import cached_property
from wsgiref.util import FileWrapper

from miniweb.exceptions import PayloadTooLarge

from .request import HttpRequest
from .response import HttpResponse
from .router import Router

class Application(object):

    def __init__(self,):
        self.middlewares = []
        self.router = Router()
        self.global_permitted_methods = []

    def set_middlewares(self, middlewares):
        self.middlewares = [] + middlewares

    @cached_property
    def dispatch_chain(self):
        dispatch = self.dispatch
        for middleware_class in reversed(self.middlewares):
            dispatch = middleware_class(dispatch)
        return dispatch

    def dispatch(self, http_request, http_response):
        if self.global_permitted_methods and (not http_request.method in self.global_permitted_methods):
            http_response.not_allowed(method=http_request.method, permitted_methods=self.global_permitted_methods)
        else:
            handler = self.router.dispatch(http_request.path)
            if not handler:
                http_response.not_found()
            else:
                try:
                    handler(http_request, http_response)
                except PayloadTooLarge as error:
                    http_response.payload_too_large(error.args[0], error.args[1])

    def __call__(self, env, start_response):
        request = HttpRequest(env, application=self)
        response = HttpResponse(start_response, request=request, application=self)
        self.dispatch_chain(request, response)
        return self.do_final_response(request, response)

    def do_final_response(self, request, response):
        response.start_response(response.final_status_code, response.final_headers)
        final_content = response.final_content
        if not final_content:
            return []
        if isinstance(final_content, FileWrapper):
            return final_content
        return [final_content]