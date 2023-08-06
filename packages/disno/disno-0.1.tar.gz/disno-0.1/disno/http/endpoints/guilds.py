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
from ..utils import bytes_to_base64_data

from typing import Optional

class GuildEndpoints:
    def create_guild(
        self,
        *,
        name: str,
        icon: Optional[bytes] = None,
        verification_level: Optional[int] = None,
        default_message_notifications: Optional[int] = None,
        explicit_content_filter: Optional[int] = None,
        roles = None,
        channels = None,
        afk_channel_id: Optional[int] = None,
        afk_timeout: Optional[int] = None,
        system_channel_id: Optional[int] = None,
        system_channel_flags: Optional[int] = None,
    ):
        r = Route('POST', '/guilds')

        payload = {
            "name": str(name),
            "icon": bytes_to_base64_data(icon),
            "verification_level": verification_level,
            "default_message_notifications": default_message_notifications,
            "explicit_content_filter": explicit_content_filter,
            "roles": roles,
            "channels": channels,
            "afk_channel_id": afk_channel_id,
            "afk_timeout": afk_timeout,
            "system_channel_id": system_channel_id,
            "system_channel_flags": system_channel_flags,
        }

        return self.request(r, payload=payload)

    def get_guild(
        self,
        guild_id: int,
        *,
        with_counts: Optional[bool] = False
    ):
        r = Route('GET', '/guilds/{guild_id}', guild_id=guild_id)

        params = {
            "with_counts": int(with_counts),
        }

        return self.request(r, params=params)
