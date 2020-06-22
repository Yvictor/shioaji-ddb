import redis
import msgpack
import dolphindb


class RedisQuoteManager:
    def __init__(self, rs: redis.Redis):
        self.rs = rs

    def on_quote(self, topic: str, quote: dict):
        self.rs.rpush(topic, msgpack.dumps(quote))


class DDBQuoteManager:
    def __init__(self, ddb: dolphindb.session):
        self.ddb = ddb
