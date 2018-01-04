from aiohttp import web

from git_shell_prompt.server.formatters import base


class Bash(base.Formatter):
    specs = 'bash',

    @classmethod
    def format(cls, root, **info):
        return web.Response(text=f'{root}>')
