import aiohttp
import asyncio
from collections import namedtuple, deque
import concurrent.futures
import logging
import sys
import time

from .websockets import ClientWebsocket
from .http import HTTPClient

class Client:
    def __init__(self, loop=None):
        self.session = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        user_agent = 'DiscordBot (https://github.com/QwireTeam/disno {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format("0.0.1", sys.version_info, aiohttp.__version__)

        self.http = HTTPClient(self)
        self.ws = None

    async def login(self, token):
        data = await self.session.request('GET', 'https://discord.com/api/v9/users/@me', **{
            "headers":{
                "User-Agent": self.user_agent,
                "X-Ratelimit-Precision": "millisecond",
                "Authorization": f"Bot {token}"
            }
        })
        print(await data.json())
    
    async def connect(self):
        ws_params = {
            'initial': True,
            'shard_id': None,
        }
        self.ws = await ClientWebsocket.initialize(client=self)
        while True:
            await self.ws.poll_receive()

    async def start(self, token):
        await self.login(token)
        await self.connect()
    
    def run(self, token):
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.token = token
        async def runner():
            await self.start(token=token)
        future = asyncio.ensure_future(runner(), loop=self.loop)
        self.loop.run_forever()

