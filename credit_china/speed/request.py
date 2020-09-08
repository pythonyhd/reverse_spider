import asyncio
import time

import aiohttp
import httpx
import requests
from fake_useragent import UserAgent

headers = {'User-Agent': UserAgent().chrome}


def requests_(url):
    resp = requests.get(url, headers=headers, timeout=15, allow_redirects=False)
    if resp.status_code == 200:
        return resp.json()


def httpx_(url):
    resp = httpx.get(url, headers=headers, timeout=15, allow_redirects=False)
    if resp.status_code == 200:
        return resp.json()


async def asy_httpx(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.json()


async def asy_aio(url):
    async with aiohttp.ClientSession() as client:
        resp = await client.get(url)
        result = await resp.json()
        return result


def make_request(session, url):
    resp = session.get(url, headers=headers, timeout=15, allow_redirects=False)
    return resp.json()


def main_request(url):
    session = requests.session()
    start = time.time()
    for _ in range(10):
        make_request(session, url)
    end = time.time()
    print(f'保持连接耗时：{end - start}')


async def make_httpx(client, url):
    resp = await client.get(url, headers=headers, timeout=15, allow_redirects=False)
    return resp.json()


async def main_httpx(url):
    async with httpx.AsyncClient() as client:
        start = time.time()
        task_list = []
        for _ in range(10):
            req = make_httpx(client, url)
            task = asyncio.create_task(req)
            task_list.append(task)

        await asyncio.gather(*task_list)
        end = time.time()
        print(f'httpx异步耗时：{end - start}')


if __name__ == '__main__':
    link = 'http://httpbin.org/get'
    # res = requests_(url=link)
    # print(res)
    # htpx = httpx_(url=link)
    # print(htpx)
    # asy_htp = asyncio.run(asy_httpx(link))
    # print(asy_htp)
    # aio_htp = asyncio.run(asy_aio(link))
    # print(aio_htp)
    start = time.time()
    for _ in range(10):
        # requests_(link)
        httpx_(link)
    end = time.time()
    # print(f'requests不保持连接耗时：{end - start}')
    print(f'httpx耗时：{end - start}')

    # main_request(link)
    asyncio.run(main_httpx(link))