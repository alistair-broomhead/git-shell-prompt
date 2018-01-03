import os
import asyncio
import pathlib

import aiohttp
import click

from git_shell_prompt import synchronisation


def resolve(async_call):
    future = asyncio.ensure_future(async_call)

    asyncio.get_event_loop().run_until_complete(future)

    return future.result()


async def get(url):
    """
    This is somewhat overkill, but aiohttp is a requirement
    and requests is not...
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


def git_dir(path):
    path = pathlib.Path(path).resolve()

    if path.is_file():
        path = path.parent

    return path


class Client(synchronisation.Client):

    def get(self, host='127.0.0.1', path='.'):
        port = self.port
        path = str(git_dir(path)).lstrip('/')
        url = f'http://{host}:{port}/{path}'
        request = get(url)
        response = resolve(request)

        return response


def trace(frame, event, arg):
    return trace


def set_trace():
    import sys
    sys.settrace(trace)


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--sync-file', default=synchronisation.DEFAULT_SYNC_FILE)
def main(host, sync_file):
    print(Client(sync_file).get(host, os.getcwd()))


if __name__ == '__main__':
    main()
