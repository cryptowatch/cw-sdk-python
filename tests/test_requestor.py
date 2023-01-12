import requests
import pytest

from cryptowatch import rest_endpoint

import cryptowatch


def test_set_api_key_programmatically(requests_mock):
    cryptowatch.api_key = "ABC"
    requests_mock.get(
        "{}/assets/{}".format(rest_endpoint, "btc"),
        status_code=200,
        text="""{
          "result": {
            "id": 60,
            "symbol": "btc",
            "name": "Bitcoin",
            "fiat": false,
            "markets": {
              "base": [
                {
                  "id": 1,
                  "exchange": "bitfinex",
                  "pair": "btcusd",
                  "active": true,
                  "route": "https://api.cryptowat.ch/markets/bitfinex/btcusd"
                }]
            }
          },
          "allowance": {
                "cost": 40277,
                "remaining": 3959423007,
                "remainingPaid": 0
              }
          }""",
    )
    bitcoin = cryptowatch.assets.get("btc")
    assert bitcoin._http_response.request.headers.get("X-CW-API-Key") == "ABC"


def test_resource_not_found(requests_mock):
    # Assets
    asset_symbol = "yetanothershitcoin"
    requests_mock.get(
        "{}/assets/{}".format(rest_endpoint, asset_symbol),
        status_code=404,
        text='{"error": "foo"}',
    )
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError) as ex:
        cryptowatch.assets.get(asset_symbol)
    assert ex.value._message == "foo"
    # Instruments
    instrument_symbol = "shitcoin1shitcoin2"
    requests_mock.get(
        "{}/pairs/{}".format(rest_endpoint, instrument_symbol),
        status_code=404,
        text='{"error": "foo_instruments"}',
    )
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError) as ex:
        cryptowatch.instruments.get(instrument_symbol)
    assert ex.value._message == "foo_instruments"
    # Exchanges
    exchange = "nyse"
    requests_mock.get(
        "{}/exchanges/{}".format(rest_endpoint, exchange),
        status_code=404,
        text='{"error": "foo_exchanges"}',
    )
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError) as ex:
        cryptowatch.exchanges.get(exchange)
    assert ex.value._message == "foo_exchanges"
    # Markets
    market = "nyse:googusd"
    requests_mock.get(
        "{}/markets/{}/{}/summary".format(rest_endpoint, *market.split(":")),
        status_code=404,
        text='{"error": "foo_markets"}',
    )
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError) as ex:
        cryptowatch.markets.get(market)
    assert ex.value._message == "foo_markets"


def test_allowance_exceeded(requests_mock):
    asset_symbol = "btc"
    requests_mock.get(
        "{}/assets/{}".format(rest_endpoint, asset_symbol),
        status_code=429,
        text='{"error": "接口信用不足"}',
    )
    with pytest.raises(cryptowatch.errors.APIRateLimitError) as ex:
        cryptowatch.assets.get(asset_symbol)
    assert ex.value._message == "接口信用不足"


def test_server_error(requests_mock):
    # Server returning HTTP 500 INTERNAL SERVER ERROR
    asset_symbol = "btc"
    requests_mock.get(
        "{}/assets/{}".format(rest_endpoint, asset_symbol),
        status_code=500,
        text='{"error": "bad"}',
    )
    with pytest.raises(cryptowatch.errors.APIServerError):
        cryptowatch.assets.get(asset_symbol)
    # Server returning HTTP 502 BAD GATEWAY
    asset_symbol = "ltc"
    requests_mock.get(
        "{}/assets/{}".format(rest_endpoint, asset_symbol),
        status_code=502,
        text='{"error": "bad"}',
    )
    with pytest.raises(cryptowatch.errors.APIServerError):
        cryptowatch.assets.get(asset_symbol)
    # Server returning HTTP 503 SERVICE UNAVAILABLE
    asset_symbol = "ltc"
    requests_mock.get(
        "{}/assets/{}".format(rest_endpoint, asset_symbol),
        status_code=503,
        text='{"error": "bad"}',
    )
    with pytest.raises(cryptowatch.errors.APIServerError) as ex:
        cryptowatch.assets.get(asset_symbol)


def test_client_error(requests_mock):
    asset_symbol = "btc"
    requests_mock.get(
        "{}/assets/{}".format(rest_endpoint, asset_symbol),
        status_code=400,
        text='{"error": "bad"}',
    )
    with pytest.raises(cryptowatch.errors.APIRequestError):
        cryptowatch.assets.get(asset_symbol)
