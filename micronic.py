import os

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from jinja2 import Environment, FileSystemLoader

_env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), 'templates')))

def render_template(template, context={}):
    t = _env.get_template(template)
    return Response(t.render(context))



class Micronic(object):
    def __init__(self):
        self.routes = Map([])

    def __call__(self, env, start_response):
        return self.wsgi_app(env, start_response)

    def wsgi_app(self, env, start_response):
        request = Request(env)
        response = self.dispatch(request)
        return response(env, start_response)


    def dispatch(self, request):
        adapter = self.routes.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return endpoint(request, **values)
        except HTTPException, e:
            return e
    
    def add_route(self, rule):
        self.routes.add(rule)

    def route(self, path, **kwargs):
        def wrapper(fun):
            self.add_route(Rule(path, endpoint=fun))
            def decorated(*args, **kwargs):
                return fun(*args, **kwargs)
            return decorated
        return wrapper

    def serve(self, debug=False, use_reloader=False):
        from werkzeug.serving import run_simple
        run_simple('127.0.0.1', 5000, SharedDataMiddleware(self.wsgi_app, {'/static': os.path.join(os.getcwd(), 'static')}), use_debugger=debug, use_reloader=use_reloader)
