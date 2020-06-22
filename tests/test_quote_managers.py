import pytest
import msgpack
from sjddb.quote_managers import RedisQuoteManager, DDBQuoteManager
from sjddb.stream_sample_data import (
    index_tse_001_tick,
    index_tse_001_bidask,
    stock_2330_tick,
    stock_2330_tick_simtrade,
    stock_2330_bidask,
    stock_2330_bidask_simtrade,
    txf_tick,
    txf_tick_simtrade,
    txf_bidask,
    txf_bidask_simtrade,
)


@pytest.fixture
def rs(mocker):
    return mocker.MagicMock()


@pytest.fixture
def rqm(rs):
    return RedisQuoteManager(rs)


topic_quote_case = [
    index_tse_001_tick,
    index_tse_001_bidask,
    stock_2330_tick,
    stock_2330_tick_simtrade,
    stock_2330_bidask,
    stock_2330_bidask_simtrade,
    txf_tick,
    txf_tick_simtrade,
    txf_bidask,
    txf_bidask_simtrade,
]


@pytest.mark.parametrize("topic, quote", topic_quote_case)
def test_redis_quote_manager_onquote(
    rqm: RedisQuoteManager, topic: str, quote: dict
):
    rqm.on_quote(topic, quote)
    rqm.rs.rpush.assert_called_once_with(topic, msgpack.dumps(quote))


if __name__ == "__main__":
    pytest.main([__file__])
