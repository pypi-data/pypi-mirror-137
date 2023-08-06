from pyppeteer import launch
from pyppeteer.browser import Browser
from .pages import PagesPool, PageItem


class BrowserPool:
    def __init__(
        self,
        options: dict = None,
        pool_size: int = 1,
        page_pool_size: int = 1,
        max_use_num: int = 5,
        **kwargs,
    ):
        self.__browser = {}
        self.__pid_usage = {}
        self.options = options
        self.pool_size = pool_size
        self.page_pool_size = page_pool_size
        self.max_use_num = max_use_num
        self.kwargs = kwargs

    async def create(self):
        for _ in range(self.pool_size):
            browser = await launch(self.options, **self.kwargs)
            pages_pool = await PagesPool(
                browser=browser,
                page_pool_size=self.page_pool_size,
                max_use_num=self.max_use_num,
            ).create()
            self.__browser[browser.process.pid] = pages_pool
            self.__pid_usage[browser.process.pid] = 0

        return self

    @property
    def less_loaded_pid(self):
        for pid, _ in sorted(self.__pid_usage.items(), key=lambda x: x[1]):
            return pid

    def acquire(self) -> PageItem:
        pid = self.less_loaded_pid
        self.__pid_usage[pid] += 1
        return PagesPoolContext(self.__browser[pid])

    @classmethod
    def replace(cls, pid: int, browser: Browser):
        pass


class PagesPoolContext:
    def __init__(self, pages_pool):
        self.__pages_pool = pages_pool
        self.__current_page = None

    async def __aenter__(self) -> PageItem:
        self.__current_page = await self.__pages_pool.get_page()
        return self.__current_page

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.__pages_pool.put_page(self.__current_page)
