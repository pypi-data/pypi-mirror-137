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

from ..route import Route
from ..enums import AuthType
from .. import utils

MISSING = utils.MISSING

class UserEndpoints:
    def get_user(self, user_id: int):
        r = Route('GET', '/users/{user_id}', user_id=user_id)
        return self.request(r)

    def get_current_user(self, token: str):
        r = Route('GET', '/users/@me')
        return self.request(r, auth=AuthType.bearer, token=token)

    def login(self, token: str = None):
        r = Route('GET', '/users/@me')
        return self.request(r, auth=AuthType.bot, token=token or self.bot_token)

    def edit_current_user(self, token: str, *, username: str = None, avatar: bytes = None):
        r = Route('PATCH', '/users/@me')
        params = {}

        if username is not None:
            params["username"] = username

        if avatar is not None:
            params["avatar"] = utils.bytes_to_base64_data(avatar)

        return self.request(r, params=params, auth=AuthType.bearer, token=token)

    def get_current_user_guilds(self, token: str, *, limit: int = 200, before: int = None, after: int = None):
        r = Route('PATCH', '/users/@me/guilds')
        params = {
            "limit": limit
        }

        if before is not None:
            params["before"] = before

        if after is not None:
            params["after"] = after

        return self.request(r, params=params, auth=AuthType.bearer, token=token)

    def get_current_user_guild_member(self, token: str, *, guild_id):
        r = Route('GET', '/users/@me/guilds/{guild_id}/member', guild_id=guild_id)
        return self.request(r, auth=AuthType.bearer, token=token)

    def remove_current_user_from_guild(self, token: str, *, guild_id):
        r = Route('DELETE', '/users/@me/guilds/{guild_id}', guild_id=guild_id)
        return self.request(r, auth=AuthType.bearer, token=token)

    def get_current_user_connections(self, token):
        r = Route('GET', '/users/@me/connections')
        return self.request(r, auth=AuthType.bearer, token=token)
