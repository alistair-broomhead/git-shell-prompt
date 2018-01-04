from aiohttp import web
from gunicorn.app import wsgiapp

from git_shell_prompt.server import git


async def handler(request):
    return web.json_response(
        await git.get_info(path=request.path)
    )


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
