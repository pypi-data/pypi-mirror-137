
import os
from miniweb.router import Router

class StaticFileService(object):
    def __init__(self, path):
        self.path = path
    
    def __call__(self, http_request, http_response):
        http_response.response_file(self.path)

class StaticIndexService(object):

    def __init__(self, path):
        self.path = path

    def __call__(self, http_request, http_response):
        dirs = [
            """<li><a href="./../">..</a></li>"""
        ]
        files = []
        for filename in os.listdir(self.path):
            filepath = os.path.abspath(os.path.join(self.path, filename))
            if os.path.isfile(filepath):
                url = f"./{filename}".replace("\\", "/")
                files.append("""<li><a href="{url}">{filename}</a></li>""".format(
                    url = url,
                    filename = filename,
                ))
            else:
                url = f"./{filename}/".replace("\\", "/")
                dirs.append("""<li><a href="{url}">{filename}</a></li>""".format(
                    url = url,
                    filename = filename,
                ))
        html = """<html>
        <head><head>
        <body><ul>
        """
        html += "\r\n".join(dirs) + "\r\n"
        html += "\r\n".join(files) + "\r\n"
        html += "</ul></body></html>"
        return http_response.response(html)

class StaticFilesRouter(Router):

    def __init__(self, root, auto_index=False):
        super().__init__()
        self.root = os.path.abspath(root)
        self.auto_index = auto_index
        self.auto_discover_urls()

    def auto_discover_urls(self):
        if self.auto_index:
            self.add_route("/", StaticIndexService(self.root))
        for root, dirs, files in os.walk(self.root):
            if self.auto_index:
                for dir in dirs:
                    dirname = os.path.abspath(os.path.join(root, dir))
                    url = "/" + os.path.relpath(dirname, self.root) + "/"
                    url = url.replace("\\", "/")
                    self.add_route(url, StaticIndexService(dirname))
            for file in files:
                filename = os.path.abspath(os.path.join(root, file))
                url = "/" + os.path.relpath(filename, self.root)
                url = url.replace("\\", "/")
                self.add_route(url, StaticFileService(filename))
