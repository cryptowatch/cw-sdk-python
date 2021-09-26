import pytest

import cryptowatch


curl "https://api.cryptowat.ch/markets/kraken/btceur/price"

def test_assets_endpoints():
    ## Testing getting one asset
    bitcoin = cryptowatch.assets.get("btc")
    # Test Asset object structure
    assert hasattr(bitcoin, "asset")
    assert hasattr(bitcoin.asset, "id")
    assert hasattr(bitcoin.asset, "fiat")
    assert hasattr(bitcoin.asset, "name")
    assert hasattr(bitcoin.asset, "symbol")
    assert hasattr(bitcoin.asset, "markets")
    assert type(bitcoin.asset.markets) == type(dict())
    assert bitcoin.asset.markets.get("base") is not None
    assert bitcoin.asset.markets.get("quote") is not None
    assert type(bitcoin.asset.markets.get("base")) == type(list())
    # test bitcoin Asset values
    assert bitcoin.asset.id == 60
    assert bitcoin.asset.name == "Bitcoin"
    assert bitcoin.asset.symbol == "btc"
    assert bitcoin.asset.fiat == False
    # Testing listing all assets
    assets = cryptowatch.assets.list()
    assert hasattr(assets, "assets")
    assert type(assets.assets) == type(list())
    assert type(assets.assets[0]) == cryptowatch.resources.assets.AssetResource
    # This should raise an APIResourceNotFoundError Exception
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError):
        cryptowatch.assets.get("shitcointhatdoesntexists")


def test_instruments_endpoints():
    ## Testing getting one instrument
    market = cryptowatch.instruments.get("btcusd")
    # Test instrument object structure
    assert hasattr(market, "instrument")
    assert hasattr(market.instrument, "id")
    assert hasattr(market.instrument, "base")
    assert hasattr(market.instrument, "quote")
    assert hasattr(market.instrument, "symbol")
    assert hasattr(market.instrument, "route")
    assert hasattr(market.instrument, "markets")
    assert type(market.instrument.base) == cryptowatch.resources.assets.AssetResource
    assert type(market.instrument.quote) == cryptowatch.resources.assets.AssetResource
    assert type(market.instrument.markets) == type(list())
    # test market instrument values
    assert market.instrument.id == 9
    assert market.instrument.symbol == "btcusd"
    assert market.instrument.base.symbol == "btc"
    assert market.instrument.quote.symbol == "usd"
    assert market.instrument.route.startswith("https")
    # Testing listing all instruments
    instruments = cryptowatch.instruments.list()
    assert hasattr(instruments, "instruments")
    assert type(instruments.instruments) == type(list())
    assert (
        type(instruments.instruments[0])
        == cryptowatch.resources.instruments.InstrumentResource
    )
    # This should raise an APIResourceNotFoundError Exception
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError):
        cryptowatch.instruments.get("instrumentthatdoesntexists")


def test_exchanges_endpoints():
    ## Testing getting one exchange
    exchange = cryptowatch.exchanges.get("kraken")
    # Test exchange object structure
    assert hasattr(exchange, "exchange")
    assert hasattr(exchange.exchange, "id")
    assert hasattr(exchange.exchange, "active")
    assert hasattr(exchange.exchange, "name")
    assert hasattr(exchange.exchange, "symbol")
    assert hasattr(exchange.exchange, "routes")
    assert type(exchange.exchange.routes) == type(dict())
    # test exchange exchange values
    assert exchange.exchange.id == 4
    assert exchange.exchange.name == "Kraken"
    assert exchange.exchange.active == True
    assert exchange.exchange.symbol == "kraken"
    # Testing listing all exchanges
    exchanges = cryptowatch.exchanges.list()
    assert hasattr(exchanges, "exchanges")
    assert type(exchanges.exchanges) == type(list())
    assert (
        type(exchanges.exchanges[0]) == cryptowatch.resources.exchanges.ExchangeResource
    )
    # This should raise an APIResourceNotFoundError Exception
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError):
        cryptowatch.exchanges.get("exchangethatdoesntexists")


def test_markets_endpoints():
    ## Testing getting one market
    market = cryptowatch.markets.get("kraken:btcusd")
    # Test market object structure
    assert hasattr(market, "market")
    assert hasattr(market.market, "price")
    assert hasattr(market.market, "volume")
    assert hasattr(market.market, "volume_quote")
    assert hasattr(market.market.price, "change")
    assert hasattr(market.market.price, "change_absolute")
    assert hasattr(market.market.price, "last")
    assert hasattr(market.market.price, "high")
    assert hasattr(market.market.price, "low")
    # test market market values
    assert market.market.price.last >= 0
    assert market.market.price.low <= market.market.price.high
    # Testing listing all markets on all exchange
    markets = cryptowatch.markets.list()
    assert hasattr(markets, "markets")
    assert type(markets.markets) == type(list())
    assert type(markets.markets[0]) == cryptowatch.resources.markets.MarketResource
    # Testing lst
    kraken_markets = cryptowatch.markets.list("kraken")
    assert len(kraken_markets.markets) < len(markets.markets)
    # This should raise an APIResourceNotFoundError Exception
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError):
        cryptowatch.markets.get("marketthatdoesntexists:shitcoinusd")


def test_markets_endpoints():
    ## Testing getting one market
    candles = cryptowatch.markets.get("kraken:btcusd", ohlc=True)
    # Test candles object structure
    assert hasattr(candles, "of_1m")
    assert hasattr(candles, "of_3m")
    assert hasattr(candles, "of_5m")
    assert hasattr(candles, "of_15m")
    assert hasattr(candles, "of_30m")
    assert hasattr(candles, "of_1h")
    assert hasattr(candles, "of_2h")
    assert hasattr(candles, "of_4h")
    assert hasattr(candles, "of_6h")
    assert hasattr(candles, "of_12h")
    assert hasattr(candles, "of_1d")
    assert hasattr(candles, "of_1w")
    assert hasattr(candles, "of_1w_monday")
    # test candles type
    assert type(candles.of_1m) == type(list())
    assert type(candles.of_1w) == type(list())
    assert type(candles.of_1w_monday) == type(list())
    # This should raise an APIResourceNotFoundError Exception
    with pytest.raises(cryptowatch.errors.APIResourceNotFoundError):
        cryptowatch.markets.get("candlesthatdoesntexists:shitcoinusd", ohlc=True)


def test_unknown_api_key():
    # Unknown API key returns 401
    cryptowatch.api_key = "123"
    with pytest.raises(cryptowatch.errors.APIRequestError):
        cryptowatch.assets.get("btc")
