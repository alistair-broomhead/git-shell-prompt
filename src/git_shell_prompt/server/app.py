from aiohttp import web
from gunicorn.app import wsgiapp

from git_shell_prompt.server import (
    formatters,
    git,
)


async def handler(request):
    fmt = request.query.get('fmt')

    info = await git.get_info(path=request.path)

    return formatters.Registry.get(fmt).format(**info)


app = web.Application()

app.router.add_get('', handler)
app.router.add_get('/{path:.+}', handler)


class StandaloneApplication(wsgiapp.WSGIApplication):
    def __init__(self, **options):
        self.options = options
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return app

    @classmethod
    def create(cls, host, port, workers):
        return cls(
            app=app,
            bind=f'{host}:{port}',
            workers=workers,
            worker_class='aiohttp.worker.GunicornWebWorker',
        )


class DebugApplication:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    # noinspection PyUnusedLocal
    @classmethod
    def create(cls, host, port, workers):
        return cls(host, port)

    def run(self):
        web.run_app(app, host=self.host, port=self.port)
