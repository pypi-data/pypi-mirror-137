import typing
from functools import cached_property
from wsgiref.util import FileWrapper

from miniweb.exceptions import PayloadTooLarge
from miniweb.exceptions import LengthRequired

from .request import HttpRequest
from .response import HttpResponse
from .response import HttpChunkResponseData
from .router import Router


class Middleware(object):
    def __init__(self, get_response:typing.Callable[[HttpRequest, HttpResponse], None]) -> None:
        self.get_response = get_response
    
    def __call__(self, http_request:HttpRequest, http_response:HttpResponse) -> None:
        return self.get_response(http_request, http_response)

class Application(object):

    def __init__(self):
        self.middlewares = []
        self.router = Router()
        self.global_permitted_methods = []

    def set_middlewares(self, middlewares:typing.List[Middleware]):
        self.middlewares = [] + middlewares

    @cached_property
    def dispatch_chain(self):
        dispatch = self.dispatch
        for middleware_class in reversed(self.middlewares):
            dispatch = middleware_class(dispatch)
        return dispatch

    def dispatch(self, http_request:HttpRequest, http_response:HttpResponse) -> None:
        if self.global_permitted_methods and (not http_request.method in self.global_permitted_methods):
            http_response.not_allowed(method=http_request.method, permitted_methods=self.global_permitted_methods)
        else:
            handler = self.router.dispatch(http_request.path)
            if not handler:
                http_response.not_found()
            else:
                try:
                    handler(http_request, http_response)
                except LengthRequired as error:
                    http_response.length_required()
                except PayloadTooLarge as error:
                    http_response.payload_too_large(error.args[0], error.args[1])

    def __call__(self, env, start_response):
        http_request = HttpRequest(env, application=self)
        http_response = HttpResponse(start_response, request=http_request, application=self)
        self.dispatch_chain(http_request, http_response)
        return self.do_final_response(http_request, http_response)

    def do_final_response(self, http_request:HttpRequest, http_response:HttpResponse):
        http_response.start_response(http_response.final_status_code, http_response.final_headers)
        final_content = http_response.final_content
        if not final_content:
            return []
        if isinstance(final_content, FileWrapper):
            return final_content
        if isinstance(final_content, HttpChunkResponseData):
            return final_content
        return [final_content]
