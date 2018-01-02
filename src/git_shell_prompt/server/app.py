from aiohttp import web
from git_shell_prompt.server import git


async def handler(request):
    return web.json_response(
        await git.get_info(path=request.path)
    )


def create_app():
    app = web.Application()

    app.router.add_get('', handler)
    app.router.add_get('/{path:.+}', handler)

    return app


def run(**kwargs):
    app = create_app()

    web.run_app(app, **kwargs)
