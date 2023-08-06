from asyncio import Queue
from pyppeteer.browser import Browser
from pyppeteer.page import Page


class PageItem:
    def __init__(self, page: Page, max_use_num: int):
        self.object = page
        self.max_use_num = max_use_num
        self.used_num = 0

    @property
    def is_need_reload(self):
        return self.used_num >= self.max_use_num

    async def convert(self, html, options=None) -> bytes:
        await self.object.setContent(html)
        return await self.object.pdf(options or {})


class PagesPool:
    def __init__(self, browser: Browser, page_pool_size: int, max_use_num: int) -> None:
        self.object = browser
        self.__pool = Queue(maxsize=page_pool_size)
        self.__max_use_num = max_use_num

    async def __new_page(self):
        page = await self.object.newPage()
        return PageItem(page, self.__max_use_num)

    async def create(self):
        default_page = await self.object.pages()

        for _ in range(self.__pool.maxsize):
            await self.__pool.put(await self.__new_page())

        if default_page:
            await default_page[0].close()

        return self

    async def get_page(self):
        page = await self.__pool.get()
        if page.is_need_reload:
            page = await self.reload_page(page)

        return page

    async def put_page(self, page):
        page.used_num += 1
        await self.__pool.put(page)

    async def reload_page(self, page):
        await page.object.close()
        return await self.__new_page()

