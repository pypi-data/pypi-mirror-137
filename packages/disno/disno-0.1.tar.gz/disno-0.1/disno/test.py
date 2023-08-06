import json

from .http import HTTPClient

client = HTTPClient("ODgxMjE1OTc3NTE2MzMxMDI4.YSpmVQ.FGK4ODoBflJkfmVmqmMK1XVjUYo")

async def func():
    print("does this even run")
    data = await client.login(
        #719980255942541362,
    )
    print(json.dumps(data, indent=2))
    #print(data._body)

async def func2():
    import aiohttp
    from discord.http import HTTPClient
    from discord.file import File
    http = HTTPClient()
    http.__session = aiohttp.ClientSession()
    http.token = "ODgxMjE1OTc3NTE2MzMxMDI4.YSpmVQ.FGK4ODoBflJkfmVmqmMK1XVjUYo"

    await http.send_files(
        796012588302991411,
        files=[File('C:\\Users\\Shams Chtioui\\Downloads\\brick.mp4')]
    )

#for i in range(10):
client.loop.run_until_complete(func())

"""
        if content is not None:
            payload["content"] = content

        if embeds is not None:
            payload["embeds"] = embeds

        if allowed_mentions is not None:
            payload["allowed_mentions"] = allowed_mentions

        if message_reference is not None:
            payload["message_reference"] = message_reference

        if components is not None:
            payload["components"] = components

        if sticker_ids is not None:
            payload["sticker_ids"] = sticker_ids

        if flags is not None:
            payload["flags"] = flags
"""