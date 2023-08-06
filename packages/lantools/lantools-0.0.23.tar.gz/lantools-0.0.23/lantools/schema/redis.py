from typing import Any
from pydantic import BaseModel
from redis import StrictRedis

class Redis(BaseModel):
    host: str
    port: int = 6379
    db: int = 0

    redis: Any = None

    def connect(self) -> StrictRedis:
        return StrictRedis(host=self.host, port=self.port, db=self.db, decode_responses=True)

    def instance(self) -> StrictRedis:
        if self.redis==None:
            self.redis = self.connect()
            return self.redis
        else:
            try:
                self.redis.ping()
                return self.redis
            except Exception as e:
                self.redis = self.connect()
                return self.redis

