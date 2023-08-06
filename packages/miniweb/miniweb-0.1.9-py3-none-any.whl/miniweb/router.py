

class Router(object):

    def __init__(self):
        self.urls = {} # url -> handler mapping
        self.names = {} # name -> url mapping

    def add_route(self, path, handler, name=None):
        """Add a path -> handler mapping to the router.

        path: Url path, e.g. /ping.
        handler: Url handler or a router instance.
            If path is an url handler, simplly add a path -> handler mapping to the router.
            If path is a router instance, add all router's mapping items to the current router.
        name: Url name for reversing the final url path.
            If the handler is a router instace, name will be ignored.
            For example, in one module,
            we created a `DebugRouter` and add a `/ping` route with a name called `ping`, 
            and then we add the `DebugRouter` as `/debug` route in the application.router,
            so finally we reverse with name `ping`,
            we got the final url equals `/debug/ping`.
        """
        if isinstance(handler, Router):
            subrouter = handler
            for subpath, handler in subrouter.urls.items():
                final_path = self.urljoin(path, subpath)
                self.urls[final_path] = handler
            for name, subpath in subrouter.names.items():
                final_path = self.urljoin(path, subpath)
                self.names[name] = final_path
        else:
            self.urls[path] = handler
            if name:
                self.names[name] = path

    def dispatch(self, path):
        """Get the handler by the url.
        """
        return self.urls.get(path, None)

    def reverse(self, name):
        """Get the url by the name.
        """
        return self.names.get(name)

    def urljoin(self, url, suburl):
        """Join parent url and suburl.
        """
        url = url + "/" + suburl
        url = url.replace("///", "/").replace("//", "/")
        if not url.startswith("/"):
            url = "/" + url
        return url
