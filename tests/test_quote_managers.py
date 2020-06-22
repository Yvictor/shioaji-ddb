import pytest
import msgpack
from sjddb.quote_managers import RedisQuoteManager, DDBQuoteManager
from sjddb.utils import flatten_tick
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


@pytest.mark.parametrize(
    "tick, index, expected",
    [
        [
            stock_2330_tick_simtrade[1],
            0,
            {
                "AmountSum": 0.0,
                "Close": 314.5,
                "Date": "2020/06/22",
                "Simtrade": 1,
                "TickType": 0,
                "Time": "08:59:59.885851",
                "VolSum": 0,
                "Volume": 2513,
                "index": 0,
            },
        ],
        [
            stock_2330_tick[1],
            0,
            {
                "AmountSum": 791282000.0,
                "Close": 314.5,
                "Date": "2020/06/22",
                "TickType": 2,
                "Time": "09:00:01.692097",
                "VolSum": 2516,
                "Volume": 2516,
                "index": 0,
            },
        ],
    ],
)
def test_flatten_tick(tick, index, expected):
    res = flatten_tick(tick, index)
    assert res == expected


@pytest.mark.parametrize(
    "tick",
    [
        txf_tick[1],
        txf_tick_simtrade[1],
        stock_2330_tick[1],
        stock_2330_tick_simtrade[1],
    ],
)
def test_flatten_tick_check_no_list_inside(tick):
    for i, _ in enumerate(tick.get("Close", [])):
        res = flatten_tick(tick, i)
        assert all([not isinstance(v, list) for k, v in res.items()])


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
def test_redis_quote_manager_onquote(rqm: RedisQuoteManager, topic: str, quote: dict):
    rqm.on_quote(topic, quote)
    rqm.rs.rpush.assert_called_once_with(topic, msgpack.dumps(quote))


if __name__ == "__main__":
    pytest.main([__file__])
