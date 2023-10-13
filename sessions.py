# pylint: disable-all
import secrets
import datetime
import time

# TODO: Use time instead of datetime


class SessionManager:
    def __init__(self) -> None:
        self.keys = {}

    def get_key(self, expire_time=300, add_time=300, max_time=1200):
        key = SessionKey(expire_time=expire_time, add_time=add_time, max_time=max_time)
        self.keys[key.key] = key
        return key.key
    
    def is_active(self, key):
        self.purge()
        if self.keys.get(key):
            return True
        return False
    
    def purge(self):
        for key, value in self.keys:
            if not value.is_valid():
                del self.keys[key]

class SessionKey:
    def __init__(self, expire_time=300, add_time=300, max_time=1200) -> None:
        self.key = secrets.token_hex(32)
        self.expire_time = time.time() + expire_time
        self.add_time = add_time
        self.max_time = max_time
        self.total_time = self.expire_time

    def is_valid(self):
        if datetime.datetime.now() > self.expire_time or self.total_time > self.max_time:
            return False
        return True

