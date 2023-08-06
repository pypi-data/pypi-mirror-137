

import re
import json
import typing
from functools import cached_property
from urllib.parse import parse_qs
from attr import has

from fastutils import fsutils

from .exceptions import LengthRequired
from .exceptions import PayloadTooLarge

class HttpRequest(object):

    post_size_limit = 1024*1024*2
    temporary_path = None

    def __init__(self, env, application):
        self.env = env
        self.application = application
        self.read_all_content_flag = False
        self.is_content_ready = False
        self.is_files_ready = False
        self._content = None
        self._post_data = {}
        self._post_data_content = None
        self._files = {}

    @classmethod
    def set_temporary_path(cls, path):
        cls.temporary_path = path

    @classmethod
    def set_post_size_limit(cls, limit:int=1024*1024*2):
        """Set read all limit.
        
        If the content length is less the this limit setting, then read all body into memory.
        The default limit is 2MB.
        Form data size and PAYLOAD data size must less than this limit.

        """
        cls.post_size_limit = limit

    @cached_property
    def META(self):
        return self.env

    @cached_property
    def GET(self):
        data = parse_qs(self.env["QUERY_STRING"])
        for key in list(data.keys()):
            if len(data[key]) == 1:
                data[key] = data[key][0]
        return data

    @property
    def POST(self) -> typing.Dict[str, typing.Union[str, typing.List[str]]]:
        self.read_input()
        # parse_qs("a=b&a=c&b=b") => {'a': ['b', 'c'], 'b': ['b']}
        # we wants:
        # {'a': ['b', 'c'], 'b': 'b'}
        if self._post_data:
            return self._post_data
        else:
            return self._post_data_from_content

    @cached_property
    def _post_data_from_content(self):
        data = parse_qs(self._post_data_content)
        for key in list(data.keys()):
            if len(data[key]) == 1:
                data[key] = data[key][0]
        return data

    @cached_property
    def PAYLOAD(self) -> typing.Any:
        self.read_input()
        if self._post_data_content is None:
            return {}
        try:
            return json.loads(self._post_data_content)
        except json.JSONDecodeError:
            return {}

    @cached_property
    def FILES(self):
        self.read_input()
        return self._files

    @cached_property
    def COOKIES(self) -> typing.Dict[str, str]:
        cookies = {}
        for cp in self.env.get("HTTP_COOKIE", "").split("; "):
            cs = cp.split("=", maxsplit=1)
            if len(cs) > 1:
                cookies[cs[0]] = cs[1]
            else:
                cookies[cs[0]] = ""
        return cookies

    @cached_property
    def HEADERS(self) -> typing.Dict[str, typing.Union[str, list]]:
        headers = {}
        if self.content_type:
            headers["CONTENT_TYPE"] = self.content_type
        if self.content_length:
            headers["CONTENT_LENGTH"] = self.content_length
        for key, value in self.env.items():
            if key.startswith("HTTP_"):
                headers[key] = value
        return headers


    @cached_property
    def content_encoding(self) -> str:
        return "utf-8"

    @cached_property
    def content_type(self) -> typing.Optional[str]:
        return self.env.get("CONTENT_TYPE", None)

    @cached_property
    def content_length(self) -> typing.Optional[int]:
        """Get content length from request header. If the header item is missing, returns None.
        """
        result = self.env.get("CONTENT_LENGTH", None)
        if result is None:
            return None
        else:
            return int(result)

    @cached_property
    def path(self) -> str:
        return self.env.get("PATH_INFO", "/")
    
    @cached_property
    def method(self) -> str:
        return self.env.get("REQUEST_METHOD", "GET")

    @cached_property
    def boundary(self) -> typing.Optional[str]:
        if not self.content_type:
            return None
        if not self.content_type.startswith("multipart/form-data; boundary="):
            return None
        bs = re.findall("^multipart/form-data; boundary=(.*)$", self.content_type)
        if bs:
            return bs[0]
        else:
            return None

    def set_post_data_empty(self):
        self._content = b""
        self._post_data_content = b""
        self._files = {}
        self.is_content_ready = True
        self.is_files_ready = True

    def read_input(self, read_all_files=False):
        if self.is_content_ready and self.is_files_ready:
            return

        wsgi_input = self.env.get("wsgi.input", None)
        if not wsgi_input:
            # deal with no wsgi.input
            self.set_post_data_empty()
            return

        if self.content_length is None:
            # deal with content length missing
            self.set_post_data_empty()
            raise LengthRequired()

        if self.content_length > self.post_size_limit:
            # deal with payload too large
            self.set_post_data_empty()
            raise PayloadTooLarge(self.content_length, self.post_size_limit)

        if self.boundary:
            # it is multipart
            boundary_line = b"--" + self.boundary.encode("utf-8") + b"\r\n"
            boundary_end_line = b"--" + self.boundary.encode("utf-8") + b"--\r\n"
            wsgi_input_block_handler = None
            while True:
                line = wsgi_input.readline()
                if not line:
                    break
                if line == boundary_end_line:
                    if wsgi_input_block_handler:
                        wsgi_input_block_handler.done()
                        break
                elif line == boundary_line:
                    if wsgi_input_block_handler:
                        wsgi_input_block_handler.done()
                    wsgi_input_block_handler = WsgiInputBlockHandler(self, wsgi_input)
                    wsgi_input_block_handler.prepare()
                else:
                    wsgi_input_block_handler.update(line)
            return
        else:
            # it is not multipart
            self._content = wsgi_input.read()
            self._post_data_content = self._content.decode(self.content_encoding)
            self._files = {}
            self.is_content_ready = True
            self.is_files_ready = True
            return

class WsgiInputBlockHandler(object):
    
    class BlockType:
        FormData = "form-data"
        FileData = "file-data"
    
    def __init__(self, http_request, wsgi_input):
        self.http_request = http_request
        self.wsgi_input = wsgi_input
        self.header_lines = []
        self.block_type = None
        self.block_name = None
        self.block_encoding = "utf-8"
        self.filename = None
        self.file = None

    def prepare(self):
        self.read_headers()
        self.parse_headers()
    
    def parse_headers(self):
        block_type_line_pattern = re.compile(b'Content-Disposition: form-data; name="(?P<name>[^;]+)"(; filename="(?P<filename>.+)")?\r\n')

        for line in self.header_lines:
            result = block_type_line_pattern.match(line)
            if result:
                info = result.groupdict()
                if info["filename"]:
                    self.block_type = self.BlockType.FileData
                    self.filename = info["filename"].decode("utf-8")
                    self.file = HttpRequestFile(original_filename=self.filename, workspace=self.http_request.temporary_path)
                    self.file.open("wb")
                    self.file_lastline = None
                else:
                    self.block_type = self.BlockType.FormData
                    self.filename = None
                self.block_name = info["name"].decode("utf-8")
                continue

    def read_headers(self):
        while True:
            line = self.wsgi_input.readline()
            if line == b"\r\n":
                break
            self.header_lines.append(line)

    def update(self, line):
        if self.block_type == self.BlockType.FormData:
            self.update_post_data(line)
        elif self.block_type == self.BlockType.FileData:
            self.update_file_data(line)

    def update_post_data(self, line):
        if self.block_name in self.http_request._post_data:
            if isinstance(self.http_request._post_data[self.block_name], str):
                self.http_request._post_data[self.block_name] = [self.http_request._post_data[self.block_name]] + [line[:-2].decode(self.block_encoding)]
            else:
                self.http_request._post_data[self.block_name].append(line[:-2].decode(self.block_encoding))
        else:
            self.http_request._post_data[self.block_name] = line[:-2].decode(self.block_encoding)

    def update_file_data(self, line):
        if self.file_lastline:
            self.file.fobj.write(self.file_lastline)
        self.file_lastline = line
    
    def done(self):
        if self.block_type == self.BlockType.FileData:
            self.file.fobj.write(self.file_lastline[:-2])
            self.file.fobj.seek(0, 0)
            self.http_request._files[self.block_name] = self.file

class HttpRequestFile(fsutils.TemporaryFile):
    
    def __init__(self, original_filename, *args, **kwargs):
        self.original_filename = original_filename
        super().__init__(*args, **kwargs)
