import abc
import typing

from aiohttp import web


JSON = typing.Union[int, str, None, typing.Dict[str, 'JSON']]


class Formatter(abc.ABC):
    @property
    @abc.abstractmethod
    def specs(self) -> typing.Tuple[str]:
        return '',

    @classmethod
    @abc.abstractmethod
    def format(cls, **info: typing.Dict[str, JSON]) -> web.Response:
        return web.json_response(info)
