from base64 import b64encode
from urllib.parse import quote as uriquote

try:
    import orjson

    to_json = lambda o: orjson.dumps(o).decode('utf-8')
    from_json = orjson.loads
except ModuleNotFoundError:
    import json

    to_json = lambda o: json.dumps(o, separators=(',', ':'), ensure_ascii=True)
    from_json = json.loads

class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __repr__(self):
        return "<nothing here>"

MISSING = _MissingSentinel()

def get_mime_type_for_image(data: bytes):
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data[0:3] == b'\xff\xd8\xff' or data[6:10] in (b'JFIF', b'Exif'):
        return 'image/jpeg'
    elif data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'
    else:
        raise TypeError('Unsupported image type given')

def bytes_to_base64_data(data: bytes):
    mime = get_mime_type_for_image(data)
    b64 = b64encode(data).decode('ascii')
    return 'data:{mime};base64,{data}'.format(mime=mime, data=b64)
