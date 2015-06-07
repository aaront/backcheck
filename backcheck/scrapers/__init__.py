# -*- coding: utf-8 -*-

import urllib.parse
import asyncio

import aiohttp
import lxml.html
import lxml.html.clean


class BaseAsyncScraper(object):
    def __init__(self, concurrency: int=10):
        self.urls = []
        self.concurrency = concurrency
        self.pages = []

    @staticmethod
    def _format_url(base: str, data: dict):
        return '{0}?{1}'.format(base, urllib.parse.urlencode(data))

    def _process(self, params: dict, page: bytes):
        raise NotImplementedError()

    @asyncio.coroutine
    def _fetch(self, *args, **kwargs):
        response = yield from aiohttp.request('GET', *args, **kwargs)
        return (yield from response.read())

    @asyncio.coroutine
    def _buffer(self, sem: asyncio.Semaphore, base: str, data: dict):
        url = self._format_url(base, data)
        with (yield from sem):
            page = yield from self._fetch(url)
        tree = lxml.html.fromstring(lxml.html.clean.clean_html(page.decode('utf-8', 'ignore')))
        self.pages.append(self._process(data, tree))

    def _get(self, base: str, urls: list):
        sem = asyncio.Semaphore(self.concurrency)
        loop = asyncio.get_event_loop()
        f = asyncio.wait([self._buffer(sem, base, url) for url in urls])
        loop.run_until_complete(f)
        return self.pages

    def get(self, *args, **kwargs):
        raise NotImplementedError()
