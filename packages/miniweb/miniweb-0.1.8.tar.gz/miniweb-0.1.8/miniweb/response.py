import os
import uuid
import time
import datetime
from urllib.parse import quote
from wsgiref.util import FileWrapper

class HttpResponse(object):

    DEFAULT_FORBIDDEN_MESSAGE = """<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
</body>
</html>
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->"""

    DEFAULT_NOT_FOUND_MESSAGE = """<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>The request url {path} is NOT found.</center>
</body>
</html>
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->"""

    DEFAULT_NOT_ALLOWED_MESSAGE = """<html>
<head><title>405 Method Not Allowed</title></head>
<body>
<center><h1>405 Method Not Allowed</h1></center>
<hr><center>The {method} method is NOT in permitted.</center>
</body>
</html>
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->"""

    DEFAULT_PAYLOAD_TOO_LARGE_MESSAGE = """<html>
<head><title>413 Payload Too Large</title></head>
<body>
<center><h1>413 Payload Too Large</h1></center>
<hr><center>The content length ({content_length}) is larger than the payload max size limit {payload_max_size_limit}.</center>
</body>
</html>
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->"""

    DEFAULT_LENGTH_REQUIRED_MESSAGE = """<html>
<head><title>411 Length Required</title></head>
<body>
<center><h1>411 Length Required</h1></center>
<hr><center>Post request requires Content-Length header.</center>
</body>
</html>
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->
<!-- a padding to disable MSIE and Chrome friendly error page -->"""

    HTTP_STATUS_CODES = {
        100: "Continue",
        101: "Switching Protocols",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Payload Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        416: "Range Not Satisfiable",
        417: "Expectation Failed",
        426: "Upgrade Required",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
    }

    def __init__(self, start_response, request, application):

        self.start_response = start_response
        self.request = request
        self.application = application

        self.status_code = 200
        self.headers = {}
        self.cookies = {}
        self.content = None
        self.content_type = None
        self.content_encoding = "utf-8"

    def set_header(self, name, value, multiple=False):
        """Set response header.

        name: Header name.
        value Header value.
        multiple: If multiple==True, set the header many times. For example Set-Cookie header can be set many times.

        # ######################################################################
        # The header value must be plain ascii characters, so it shoud be encoded before assign to a header.
        # You can use uri quote or base64 to do the string encode.
        # ######################################################################

        Examples:

        from urllib.parse import quote
        http_response.set_header("user-name", quote("张三"))

        """
        name = name.lower()
        if not name in self.headers:
            self.headers[name] = []
        if multiple:
            self.headers[name].append(value)
        else:
            self.headers[name] = [value]
        return name, self.headers[name]

    def set_cookie(self, name:str, value:str, expires:datetime.datetime=None, max_age:int=None, domain:str=None, path:str="/", secure:bool=True, httpOnly:bool=True, sameSite:str=None):
        cookie_name, cookie_value = self.make_cookie(name, value, expires, max_age, domain, path, secure, httpOnly, sameSite)
        self.cookies[cookie_name] = cookie_value
        return cookie_name, cookie_value

    @classmethod
    def make_cookie(cls, name:str, value:str, expires:datetime.datetime=None, max_age:int=None, domain:str=None, path:str="/", secure:bool=True, httpOnly:bool=True, sameSite:str=None):
        name = quote(name)
        value = quote(value)
        cookie_parts = [f"{name}={value}"]
        if expires:
            expires = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(expires.timestamp()))
            cookie_parts.append(f"Expires={expires}")
        if max_age:
            cookie_parts.append(f"Max-Age={max_age}")
        if domain:
            cookie_parts.append(f"Domain={domain}")
        if path:
            cookie_parts.append(f"Path={path}")
        if sameSite:
            cookie_parts.append(f"SameSite={sameSite}")
        if secure:
            cookie_parts.append("Secure")
        if httpOnly:
            cookie_parts.append("HttpOnly")
        cookie_text = "; ".join(cookie_parts)
        return name, cookie_text

    @property
    def final_headers(self):
        if self.content_type and (not "content-type" in self.headers):
            self.set_header("content-type", self.content_type)
        if not "set-cookie" in self.headers:
            for _, cookie_value in self.cookies.items():
                self.set_header("set-cookie", cookie_value, multiple=True)
        results = []
        for header_name, header_values in self.headers.items():
            for header_value in header_values:
                results.append((header_name.title(), header_value))
        return results

    @property
    def final_status_code(self):
        return "{status_code} {status_description}".format(
            status_code=self.status_code,
            status_description=self.HTTP_STATUS_CODES.get(self.status_code, "Unknown Status"),
        )

    @property
    def final_content(self):
        if self.content is None:
            return None
        if isinstance(self.content, FileWrapper):
            return self.content
        if isinstance(self.content, bytes):
            return self.content
        if isinstance(self.content, str):
            return self.content.encode(self.content_encoding)
        return str(self.content).encode(self.content_encoding)

    # 301
    def redirect_permanent(self, url, status_code=301):
        self.status_code = status_code
        self.set_header("location", url)
        return self
    
    # 302
    def redirect_temporary(self, url, status_code=302):
        self.status_code = status_code
        self.set_header("location", url)
        return self

    # alias for 301 & 302
    def redirect(self, url, permanent=False):
        if permanent:
            return self.redirect_permanent(url)
        else:
            return self.redirect_temporary(url)

    # 403
    def forbidden(self, message=None, status_code=403, content_type="text/html"):
        self.status_code = status_code
        self.content_type = content_type
        self.content = message or self.DEFAULT_FORBIDDEN_MESSAGE
        return self

    # 404
    def not_found(self, message=None, status_code=404, content_type="text/html"):
        self.status_code = status_code
        self.content_type = content_type
        self.content = message or self.DEFAULT_NOT_FOUND_MESSAGE.format(path=self.request.path)
        return self

    # 405
    def not_allowed(self, method, permitted_methods, message=None, status_code=405, content_type="text/html"):
        self.status_code = status_code
        self.content_type = content_type
        self.set_header("allow", ", ".join(permitted_methods))
        self.content = message or self.DEFAULT_NOT_ALLOWED_MESSAGE.format(method=method, permitted_methods=permitted_methods)
        return self

    # 411
    def length_required(self, message=None, status_code=411, content_type="text/html"):
        self.status_code = status_code
        self.content_type = content_type
        self.content = message or self.DEFAULT_LENGTH_REQUIRED_MESSAGE
        return self
    # 413
    def payload_too_large(self, content_length, payload_max_size_limit, message=None, status_code=413, content_type="text/html"):
        self.status_code = status_code
        self.content_type = content_type
        self.content = message or self.DEFAULT_PAYLOAD_TOO_LARGE_MESSAGE.format(content_length=content_length, payload_max_size_limit=payload_max_size_limit)
        return self

    # 200
    def response_html(self, content, status_code=200, content_type="text/html"):
        self.status_code = status_code
        self.content_type = content_type
        self.content = content
        return self

    # 200
    response = response_html

    # 200
    def response_text(self, content, status_code=200, content_type="text/plain"):
        self.status_code = status_code
        self.content_type = content_type
        self.content = content
        return self

    # 200
    def response_file(self, thefile, filename=None, chunk=4096, status_code=200, content_type="application/octet-stream"):
        """Response a file.

        thefile: A file path or a opened file object.
        filename: Sugguest filename for downloaded file.
            If filename is None and thefile is a file path,
            then the file's basename will be used.
            If filename is None and thefile is a opened file instance,
            then the name attr value of thefile is used a the file's path.
            If filename is None and thefile is a opened file instance but failed to get the value of it's name attr,
            then the TIMESTAMP.dat will be used.
            The TIMESTAMP is the current timestamp integer value.
        chunk: Chunk size. Default to 4096 bytes.

        Examples:

        http_response.response_file("/tmp/a.txt")
        
        fobj = open("/tmp/a.txt", "rb")
        http_response.response_file(fobj, "hello world.txt")


        """
        if isinstance(thefile, str):
            fobj = open(thefile, "rb")
            filename = filename or os.path.basename(thefile)
        else:
            fobj = thefile
            if not filename:
                filename = getattr(fobj, "name", None)
                if filename:
                    filename = os.path.basename(filename)
            if not filename:
                filename = getattr(fobj, "filename", None)
                if filename:
                    filename = os.path.basename(filename)
            if not filename:
                filename = getattr(fobj, "filepath", None)
                if filename:
                    filename = os.path.basename(filename)
            if not filename:
                filename = int(time.time()) + ".dat"
        filename = quote(filename)
        self.status_code = status_code
        self.content_type = content_type
        self.set_header("content-disposition", "attachment; filename={}".format(filename))
        self.content = FileWrapper(fobj, chunk)
        return self
