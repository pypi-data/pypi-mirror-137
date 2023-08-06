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

import aiohttp
from typing import List

from ..route import Route
from .. import utils

MISSING = utils.MISSING

class MessageEndpoints:
    def get_messages(
        self,
        channel_id,
        *,
        limit: int = 50,
        around: int = None,
        before: int = None,
        after: int = None,
    ):
        r = Route('GET', '/channels/{channel_id}/messages', channel_id=channel_id)
        params = {
            "limit": limit,
        }

        if around is not None:
            params["around"] = around

        if before is not None:
            params["before"] = before

        if after is not None:
            params["after"] = after

        return self.request(r, params=params)

    def get_message(self, channel_id: int, message_id: int):
        r = Route('GET', '/channels/{channel_id}/messages/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(r)

    def _prepare_form(self, payload, files):
        form = []
        attachments = []

        for index, file in enumerate(files):
            attachments.append(
                {
                    'id': index,
                    'filename': file['filename'],
                    'description': "a meme"
                }
            )
            form.append(
                {
                    'name': 'files[%s]' % index,
                    'value': file['fp'],
                    'filename': file['filename'],
                    'content_type': 'application/octet-stream'
                }
            )
        payload['attachments'] = attachments
        form_data = aiohttp.FormData(quote_fields=False)
        form_data.add_field('payload_json', utils.to_json(payload))
        for f in form:
            form_data.add_field(
                f['name'],
                f['value'],
                filename=f['filename'],
                content_type=f['content_type']
            )
        return form_data

    def send_message(
        self,
        channel_id: int,
        *,
        content: str = None,
        tts: bool = False,
        embeds = None,
        allowed_mentions = None,
        message_reference = None,
        components = None,
        sticker_ids: List[int] = None,
        flags: int = None,
        files = None
    ):
        r = Route('POST', '/channels/{channel_id}/messages', channel_id=channel_id)

        payload = {
            "content": content,
            "tts": int(tts),
            "embeds": embeds or [],
            "message_reference": message_reference,
            "allowed_mentions": allowed_mentions,
            "components": components,
            "sticker_ids": sticker_ids or [],
            "flags": flags,
        }

        if files is not None:
            form = self._prepare_form(payload, files)
            return self.request(r, data=form)
        else:
            return self.request(r, payload=payload)

    def edit_message(
        self,
        channel_id: int,
        message_id: int,
        *,
        content: str = MISSING,
        embeds: List = MISSING,
        flags: int = MISSING,
        allowed_mentions = MISSING,
        components: List = MISSING,
        files = MISSING
    ):
        r = Route('PATCH', '/channels/{channel_id}/messages/{message_id}', channel_id=channel_id, message_id=message_id)

        payload = {
            "content": content,
            "embeds": embeds or [],
            "allowed_mentions": allowed_mentions,
            "components": components,
            "flags": flags,
        }

        if files is not MISSING:
            form = self._prepare_form(payload, files)
            return self.request(r, data=form)
        else:
            return self.request(r, payload=payload)

    def delete_message(self, channel_id: int, message_id: int, reason: str = None):
        r = Route('DELETE', '/channels/{channel_id}/messages/{message_id}', channel_id=channel_id, message_id=message_id)
        return self.request(r, reason=reason)

    def delete_messages(self, channel_id: int, *, messages: List[int] = None, reason: str = None):
        r = Route('POST', '/channels/{channel_id}/messages/bulk-delete', channel_id=channel_id)
        payload = {
            "messages": messages,
        }

        return self.request(r, payload=payload, reason=reason)

    def crosspost_message(self, channel_id: int, message_id: int):
        r = Route('POST', '/channels/{channel_id}/messages/{message_id}/crosspost', channel_id=channel_id, message_id=message_id)
        return self.request(r)
