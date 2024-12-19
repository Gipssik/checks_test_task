class AsyncRedisMock:
    def __init__(self, cache):
        self.cache = cache or {}

    async def get(self, name):
        if name in self.cache:
            return self.cache[name]
        return None

    async def set(self, name, value, *args, **kwargs):
        if self.cache is not None:
            self.cache[name] = value
            return "OK"
        return "{}"

    async def hget(self, hash_, key):
        if hash_ in self.cache:
            if key in self.cache[hash_]:
                return self.cache[hash_][key]
        return "{}"

    async def hset(self, hash_, key, value, *args, **kwargs):
        if self.cache:
            self.cache[hash_][key] = value
            return 1
        return None

    async def exists(self, key):
        if key in self.cache:
            return 1
        return 0

    async def close(self):
        return

    async def delete(self, *keys):
        for key in keys:
            if key in self.cache:
                del self.cache[key]

    async def scan_iter(self, *args, **kwargs):
        return []
