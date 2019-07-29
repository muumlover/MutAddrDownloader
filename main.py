#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/7/26 17:09
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : MutAddrDownloader
@FileName: main.py.py
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 

"""
import logging
import os
import sys

import aiofiles as aiofiles
import aiohttp as aiohttp

block = 10 * 1024 * 1024
url = 'http://mirrors.163.com/centos/7.6.1810/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso'

filename = os.path.basename(url)


class Downloader:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'Accept-Encoding': 'deflate, gzip'
    }

    def __init__(self, conn_timeout=10, read_timeout=1800):
        self.tries = 0
        self.session = aiohttp.ClientSession(conn_timeout=conn_timeout, read_timeout=read_timeout)

    async def conti_check(self, url):
        while True:
            try:
                headers = self.headers.copy()
                headers['Range'] = 'bytes=0-4'
                resp = await self.session.request("GET", url, headers=headers)
                return bool(resp.headers.get('Content-Range'))
            except Exception as e:
                self.logger.error("error error")
                self.logger.error(f"Failed to check: {e}")
                self.logger.error("error error")
                if self.tries < 2:
                    self.tries += 1
                else:
                    raise e

    async def download(self, url):
        if os.path.exists(filename) and await conti_check(url):
            f = await aiofiles.open(filename, "ab")
            received = await f.tell()
