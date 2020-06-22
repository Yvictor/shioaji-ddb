import redis
import msgpack
import dolphindb

from sjddb.utils import flatten_tick


class RedisQuoteManager:
    def __init__(self, rs: redis.Redis):
        self.rs = rs

    def on_quote(self, topic: str, quote: dict):
        self.rs.rpush(topic, msgpack.dumps(quote))


class DDBQuoteManager:
    def __init__(self, ddb: dolphindb.session):
        self.ddb = ddb

    def on_quote(self, topic: str, quote: dict):
        if topic.startswith("L") or topic.startswith("MKT"):
            for index, _ in enumerate(quote.get("Code", [])):
                tick = flatten_tick(quote, index)
                # push tick
