from aiohttp import web

from git_shell_prompt.server.formatters import base


class JSON(base.Formatter):
    specs = 'json',

    @classmethod
    def format(cls, **info):
        return web.json_response(info)
