from os import environ


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_KEY_PREFIX = 'wrive.cache.'
SIMPLE_API_ACCESS_KEY = None


_locals = locals()


for key in _locals.keys():
    if key.isupper():
        value = environ.get(key)
        if value:
            _locals[key] = value
