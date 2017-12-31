import functools

import aiohttp.web

app = aiohttp.web.Application()


run = functools.partial(aiohttp.web.run_app, app)
