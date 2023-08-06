from urllib.parse import quote as _quote

class Route:
    base = "https://discord.com/api/v9"

    def __init__(self, method, path, **params):
        self.method = method
        self.path = path
        if params:
            self.path = self.path.format_map({k: _quote(v) if isinstance(v, str) else v for k, v in params.items()})
        self.url = self.base + self.path

    @property
    def bucket(self):
        return f"{self.method}:{self.path}"
