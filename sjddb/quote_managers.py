import redis
import msgpack
import dolphindb
import pandas as pd
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
        if topic.startswith("L"):  # or topic.startswith("MKT"):
            ticks = []
            for index, _ in enumerate(quote.get("Close", [])):
                tick = flatten_tick(quote, index)
                tick["SubSeq"] = tick["index"]
                tick["Exchange"] = "TFE"
                tick["Date"] = tick["Date"].replace("/", ".")
                tick["Time"] = tick["Time"][0:-3]
                ticks.append(tick)

            df = pd.DataFrame.from_dict(ticks, orient="columns")
            self.ddb.upload({"tStreamTickTFE": df})
            self.ddb.run(
                "objByName('StreamTickTFE').append!(select Exchange,index,Amount,AmountSum,AvgPrice,Close,Code,date(Date),DiffPrice,DiffRate,DiffType,High,Low,Open,TargetKindPrice,TickType,time(Time),TradeAskVolSum,TradeBidVolSum,VolSum,Volume from tStreamTickTFE)"
            )
