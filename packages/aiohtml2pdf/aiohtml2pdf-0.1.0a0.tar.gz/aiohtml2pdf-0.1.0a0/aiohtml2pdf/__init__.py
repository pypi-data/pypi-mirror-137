import asyncio
from .browser import BrowserPool


async def create_pool(
    options: dict = None,
    pool_size: int = 1,
    page_pool_size: int = 3,
    max_use_num: int = 5,
    **kwargs,
) -> BrowserPool:
    return await BrowserPool(
        options, pool_size, page_pool_size, max_use_num, **kwargs
    ).create()


def create_pool_without_await(
    options: dict = None,
    pool_size: int = 1,
    page_pool_size: int = 3,
    max_use_num: int = 5,
    **kwargs,
) -> BrowserPool:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        create_pool(options, pool_size, page_pool_size, max_use_num, **kwargs)
    )
