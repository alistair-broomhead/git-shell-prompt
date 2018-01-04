import asyncio


async def get_info(path):
    """Takes reassuringly long to get info ;)"""
    await asyncio.sleep(1)

    return {
        'path': path
    }
