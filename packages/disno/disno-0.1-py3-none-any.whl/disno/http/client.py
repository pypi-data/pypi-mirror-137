"""
MIT License

Copyright (c) 2021-present Qwire Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import aiohttp
import sys

from . import utils
from .enums import AuthType
from .endpoints import *

endpoints = (
    GuildEndpoints,
    UserEndpoints,
    OAuth2Endpoints,
    ChannelEndpoints,
    MessageEndpoints,
    ReactionEndpoints,
)

class AutoUnlocker:
    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback
    ) -> None:
        if self.lock.locked():
            self.lock.release()

class Requester:
    def __init__(self, session, client_id = None, client_secret = None, bot_token = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.bot_token = bot_token
        self.ratelimits = {}
        self.global_lock = asyncio.Event()
        self.global_lock.set()

        user_agent = 'DiscordBot (https://github.com/QwireDev/disno {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format("1.0.0a1", sys.version_info, aiohttp.__version__)

        self.session = session

    async def request(
        self,
        route,
        payload = None,
        params = None,
        data = None,
        reason = None,
        auth = AuthType.bot,
        token = None,
    ):
        to_pass = {}
        method = route.method
        url = route.url
        bucket = route.bucket

        lock = self.ratelimits.get(bucket, None)
        if lock is None:
            lock = asyncio.Lock()
            self.ratelimits[bucket] = lock

        headers = {
            "User-Agent": self.user_agent
        }

        if self.bot_token is not None and auth is AuthType.bot:
            headers["Authorization"] = "Bot " + self.bot_token
        elif token is not None and auth is AuthType.bearer:
            headers["Authorization"] = "Bearer " + token

        if reason is not None:
            headers["X-Audit-Log-Reason"] = utils.uriquote(reason)

        if data:
            to_pass["data"] = data
        elif payload:
            headers["Content-Type"] = "application/json"
            to_pass["data"] = utils.to_json(payload)

        if params:
            to_pass["params"] = params

        to_pass["headers"] = headers

        if not self.global_lock.is_set():
            await self.global_lock.wait()

        await lock.acquire()
        with AutoUnlocker(lock) as unlocker:
            for tries in range(5):
                async with self.session.request(method, url, **to_pass) as res:
                    data = await res.json()

                    remaining = res.headers.get("x-ratelimit-limit", None)
                    if remaining == '0' and res.status != 429:
                        delay = res.headers.get("x-ratelimit-reset-after")
                        self.loop.call_later(delay, lock.release)

                    print("received")

                    print({k:v for k,v in dict(res.headers).items() if "ratelimit" in k.lower()})
                    print(res.status)
                    print(res.headers.get('Via'))

                    if 300 > res.status >= 200:
                        return data

                    if res.status == 429:
                        reset_after = res.headers.get("x-ratelimit-reset-after")
                        is_global = data.get("global", False)

                        if is_global:
                            self.global_lock.clear()

                        await asyncio.sleep(float(reset_after))

                        if is_global:
                            self.global_lock.set()

                    return data


class HTTPClient(Requester, *endpoints):
    def __init__(self,  bot_token = None, client_id = None, client_secret = None, *, loop=None, session=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.bot_token = bot_token

        user_agent = 'DiscordBot (https://github.com/QwireDev/disno {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format("1.0.0a.1", sys.version_info, aiohttp.__version__)

        if loop is None:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

        self.loop = loop

        if session is None:
            session = aiohttp.ClientSession(loop=self.loop)

        super().__init__(session, client_id=client_id, client_secret=client_secret, bot_token=bot_token)

    async def get_gateway(self, *, encoding: str = 'json', zlib: bool = True) -> str:
        data = await self.client.session.request("GET", "https://discord.com/api/v9/gateway")
        if zlib:
            value = '{0}?encoding={1}&v=9&compress=zlib-stream'
        value = '{0}?encoding={1}&v=9'
        return value.format((await data.json())['url'], encoding)
