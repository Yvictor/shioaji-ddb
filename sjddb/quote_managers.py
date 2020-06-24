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
    CREATE_STREAM_TABLE = """
schemaTickTFE = streamTable(100:0, `Exchange`SubSeq`SimTrade`Amount`AmountSum`AvgPrice`Close`Code`Date`DiffPrice`DiffRate`DiffType`High`Low`Open`TargetKindPrice`TickType`Time`TradeAskVolSum`TradeBidVolSum`VolSum`Volume ,[SYMBOL,INT,INT,DOUBLE,DOUBLE,DOUBLE,DOUBLE,SYMBOL,DATE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,TIME,DOUBLE,DOUBLE,DOUBLE,DOUBLE]);
enableTableShareAndPersistence(table=schemaTickTFE,asynWrite=true, compress=false,cacheSize=50000, tableName="StreamTickTFE");
undef(`schemaTickTFE)
    """
    CREATE_TABLE = """
db = database("dfs://TickTFE",VALUE, today()..today()+1); 
db.createPartitionedTable(select * from StreamTickTFE,`TickTFE,`Date)
    """
    SUBSCRIBE_TABLE = """
tb_TickTFE = loadTable("dfs://TickTFE",`TickTFE)
subscribeTable(,`StreamTickTFE, "TickTFE_to_dfs", -1 , tb_TickTFE ,true)
undef(`tb_TickTFE)
    """

    def __init__(self, ddb: dolphindb.session):
        self.ddb = ddb
        self.ddb.run(self.CREATE_STREAM_TABLE)
        self.ddb.run(self.CREATE_TABLE)
        self.ddb.run(self.SUBSCRIBE_TABLE)

    def on_quote(self, topic: str, quote: dict):
        if topic.startswith("L"):  # or topic.startswith("MKT"):
            ticks = []
            for index, _ in enumerate(quote.get("Close", [])):
                tick = flatten_tick(quote, index)
                tick["SubSeq"] = tick["index"]
                tick["SimTrade"] = tick.get("SimTrade", 0)
                tick["Exchange"] = "TFE"
                tick["Date"] = tick["Date"].replace("/", ".")
                tick["Time"] = tick["Time"][0:-3]
                ticks.append(tick)

            df = pd.DataFrame.from_dict(ticks, orient="columns")
            self.ddb.upload({"tStreamTickTFE": df})
            self.ddb.run(
                "objByName('StreamTickTFE').append!(select Exchange,index,SimTrade,Amount,AmountSum,AvgPrice,Close,Code,date(Date),DiffPrice,DiffRate,DiffType,High,Low,Open,TargetKindPrice,TickType,time(Time),TradeAskVolSum,TradeBidVolSum,VolSum,Volume from tStreamTickTFE)"
            )
