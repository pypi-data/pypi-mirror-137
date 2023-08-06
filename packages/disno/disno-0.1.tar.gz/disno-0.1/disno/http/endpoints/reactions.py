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

class ReactionEndpoints:
    def create_reaction(self, channel_id: int, message_id: int, emoji: str):
        r = Route('POST', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me', channel_id=channel_id, message_id=message_id, emoji=emoji)
        return self.request(r)

    def delete_my_reaction(self, channel_id: int, message_id: int, emoji: str):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me', channel_id=channel_id, message_id=message_id, emoji=emoji)
        return self.request(r)

    def delete_reaction(self, channel_id: int, message_id: int, emoji: str, user_id: int):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}', channel_id=channel_id, message_id=message_id, emoji=emoji, user_id=user_id)
        return self.request(r)

    def get_reactions(self, *, limit = 25, after = None):
        r = Route('GET', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}')
        params = {
            "limit": limit
        }

        if after is not None:
            params["after"] = after

        return self.request(r, params=params)

    def delete_all_reactions(self, channel_id: int, message_id: int):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}/reactions', channel_id=channel_id, message_id=message_id)
        return self.request(r)

    def delete_all_reactions_for_emoji(self, channel_id: int, message_id: int, emoji: str):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}/reactions/{emoji}', channel_id=channel_id, message_id=message_id, emoji=emoji)
        return self.request(r)
