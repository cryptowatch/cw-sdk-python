from unittest import TestCase

import requests_mock

import cryptowatch
from cryptowatch import DEFAULT_REST_ENDPOINT


@requests_mock.Mocker()
class AssetsTests(TestCase):
    def setUp(self):
        self.cw = cryptowatch
        self.cw.api_key = ""

    def test_list(self, requests_mock):
        payload = """
        {
            "result": [{
                "id": 182298,
                "sid": "zer0zer0",
                "symbol": "00",
                "name": "zer0zer0",
                "fiat": false,
                "route": "https://api.cryptowat.ch/assets/00"
            }, {
                "id": 7900,
                "sid": "stone",
                "symbol": "0ne",
                "name": "Stone",
                "fiat": false,
                "route": "https://api.cryptowat.ch/assets/0ne"
            }],
            "allowance": {
                "cost": 0.015,
                "remaining": 9.94,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/assets",
            status_code=200,
            text=payload,
        )
        assets = self.cw.assets.list().assets
        self.assertEqual(2, len(assets))
        self.assertEqual("00", assets[0].symbol)
        self.assertEqual("0ne", assets[1].symbol)

    def test_get(self, requests_mock):
        asset_id = "10set"
        payload = (
            """
        {
            "result": {
                "id": 5478,
                "sid": "tenset",
                "symbol": "%s",
                "name": "Tenset",
                "fiat": false,
                "markets": {
                    "base": [{
                        "id": 299097,
                        "exchange": "uniswap-v2",
                        "pair": "10setweth",
                        "active": true,
                        "route": "https://api.cryptowat.ch/markets/uniswap-v2/10setweth"
                    }, {
                        "id": 350642,
                        "exchange": "gateio",
                        "pair": "10setusdt",
                        "active": true,
                        "route": "https://api.cryptowat.ch/markets/gateio/10setusdt"
                    }, {
                        "id": 350643,
                        "exchange": "gateio",
                        "pair": "10seteth",
                        "active": false,
                        "route": "https://api.cryptowat.ch/markets/gateio/10seteth"
                    }]
                }
            },
            "allowance": {
                "cost": 0.002,
                "remaining": 9.981,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
            % asset_id
        )
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/assets/{asset_id}",
            status_code=200,
            text=payload,
        )
        asset = self.cw.assets.get(asset_id).asset
        self.assertEqual(asset_id, asset.symbol)
        self.assertEqual("10set", asset.symbol)
        self.assertEqual("Tenset", asset.name)
        self.assertEqual(False, asset.fiat)


@requests_mock.Mocker()
class ExchangesTests(TestCase):
    def setUp(self):
        self.cw = cryptowatch
        self.cw.api_key = ""

    def test_list(self, requests_mock):
        payload = """
        {
            "result": [{
                "id": 1,
                "symbol": "bitfinex",
                "name": "Bitfinex",
                "route": "https://api.cryptowat.ch/exchanges/bitfinex",
                "active": true
            }, {
                "id": 4,
                "symbol": "kraken",
                "name": "Kraken",
                "route": "https://api.cryptowat.ch/exchanges/kraken",
                "active": true
            }],
            "allowance": {
                "cost": 0.002,
                "remaining": 9.979,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/exchanges",
            status_code=200,
            text=payload,
        )
        exchanges = self.cw.exchanges.list().exchanges
        self.assertEqual(2, len(exchanges))
        self.assertEqual("bitfinex", exchanges[0].symbol)
        self.assertEqual("kraken", exchanges[1].symbol)

    def test_get(self, requests_mock):
        exchange_id = "kraken"
        payload = (
            """
        {
            "result": {
                "id": 4,
                "symbol": "%s",
                "name": "Kraken",
                "active": true,
                "routes": {
                    "markets": "https://api.cryptowat.ch/markets/kraken"
                }
            },
            "allowance": {
                "cost": 0.002,
                "remaining": 9.977,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
            % exchange_id
        )
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/exchanges/{exchange_id}",
            status_code=200,
            text=payload,
        )
        exchange = self.cw.exchanges.get(exchange_id).exchange
        self.assertEqual(exchange_id, exchange.symbol)
        self.assertEqual("Kraken", exchange.name)


@requests_mock.Mocker()
class InstrumentsTests(TestCase):
    def setUp(self):
        self.cw = cryptowatch
        self.cw.api_key = ""

    def test_list(self, requests_mock):
        payload = """
        {
            "result": [{
                "id": 1,
                "symbol": "ethphp",
                "base": {
                    "id": 77,
                    "sid": "ethereum",
                    "symbol": "eth",
                    "name": "Ethereum",
                    "fiat": false,
                    "route": "https://api.cryptowat.ch/assets/eth"
                },
                "quote": {
                    "id": 17,
                    "sid": "philippine-peso",
                    "symbol": "php",
                    "name": "Philippine Peso",
                    "fiat": true,
                    "route": "https://api.cryptowat.ch/assets/php"
                },
                "route": "https://api.cryptowat.ch/pairs/ethphp"
            }, {
                "id": 2,
                "symbol": "ricbtc",
                "base": {
                    "id": 102,
                    "sid": "riecoin",
                    "symbol": "ric",
                    "name": "Riecoin",
                    "fiat": false,
                    "route": "https://api.cryptowat.ch/assets/ric"
                },
                "quote": {
                    "id": 60,
                    "sid": "bitcoin",
                    "symbol": "btc",
                    "name": "Bitcoin",
                    "fiat": false,
                    "route": "https://api.cryptowat.ch/assets/btc"
                },
                "route": "https://api.cryptowat.ch/pairs/ricbtc"
            }],
            "cursor": {
                "last": "M9Gs_oQYnjiD3tsB3DAbw7TBCoGas9zsFm4srNKW0fv75QLPEhPwqw",
                "hasMore": true
            },
            "allowance": {
                "cost": 0.003,
                "remaining": 9.95,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/pairs",
            status_code=200,
            text=payload,
        )
        instruments = self.cw.instruments.list().instruments
        self.assertEqual(2, len(instruments))
        self.assertEqual("ethphp", instruments[0].symbol)
        self.assertEqual("ricbtc", instruments[1].symbol)

    def test_get(self, requests_mock):
        instrument_id = "ethphp"
        payload = (
            """
        {
            "result": {
                "id": 1,
                "symbol": "%s",
                "base": {
                    "id": 77,
                    "sid": "ethereum",
                    "symbol": "eth",
                    "name": "Ethereum",
                    "fiat": false,
                    "route": "https://api.cryptowat.ch/assets/eth"
                },
                "quote": {
                    "id": 17,
                    "sid": "philippine-peso",
                    "symbol": "php",
                    "name": "Philippine Peso",
                    "fiat": true,
                    "route": "https://api.cryptowat.ch/assets/php"
                },
                "route": "https://api.cryptowat.ch/pairs/ethphp",
                "markets": [{
                    "id": 201,
                    "exchange": "quoine",
                    "pair": "ethphp",
                    "active": false,
                    "route": "https://api.cryptowat.ch/markets/quoine/ethphp"
                }, {
                    "id": 5793,
                    "exchange": "liquid",
                    "pair": "ethphp",
                    "active": false,
                    "route": "https://api.cryptowat.ch/markets/liquid/ethphp"
                }]
            },
            "allowance": {
                "cost": 0.002,
                "remaining": 9.948,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
            % instrument_id
        )
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/pairs/{instrument_id}",
            status_code=200,
            text=payload,
        )
        instrument = self.cw.instruments.get(instrument_id).instrument
        self.assertEqual(instrument_id, instrument.symbol)
        self.assertEqual("eth", instrument.base.symbol)
        self.assertEqual("Ethereum", instrument.base.name)
        self.assertEqual(False, instrument.base.fiat)
        self.assertEqual("php", instrument.quote.symbol)
        self.assertEqual("Philippine Peso", instrument.quote.name)
        self.assertEqual(True, instrument.quote.fiat)


@requests_mock.Mocker()
class MarketsTests(TestCase):
    def setUp(self):
        self.cw = cryptowatch
        self.cw.api_key = ""

    def test_list_all(self, requests_mock):
        payload = """
        {
            "result": [{
                "id": 1,
                "exchange": "bitfinex",
                "pair": "btcusd", 
                "active": true,
                "route": "https://api.cryptowat.ch/markets/bitfinex/btcusd"
            }, {
                "id": 2,
                "exchange": "bitfinex",
                "pair": "ltcusd",
                "active": true,
                "route": "https://api.cryptowat.ch/markets/bitfinex/ltcusd"
            }],
            "cursor": {
                "last": "G4yKgHf_h043IUvxZfVACNabsrpuqPjX1t1dfMBv7Wof0gbtg1CJwA",
                "hasMore": true
            },
            "allowance": {
                "cost": 0.003,
                "remaining": 9.997,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/markets",
            status_code=200,
            text=payload,
        )
        markets = self.cw.markets.list().markets
        self.assertEqual(2, len(markets))
        self.assertEqual("bitfinex", markets[0].exchange)
        self.assertEqual("btcusd", markets[0].pair)
        self.assertEqual("bitfinex", markets[1].exchange)
        self.assertEqual("ltcusd", markets[1].pair)

    def test_list_one(self, requests_mock):
        exchange = "kraken"
        payload = """
        {
            "result": [{
                "id": 86,
                "exchange": "kraken",
                "pair": "btceur",
                "active": true,
                "route": "https://api.cryptowat.ch/markets/kraken/btceur"
            }, {
                "id": 87,
                "exchange": "kraken",
                "pair": "btcusd",
                "active": true,
                "route": "https://api.cryptowat.ch/markets/kraken/btcusd"
            }],
            "allowance": {
                "cost": 0.002,
                "remaining": 9.976,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/markets/{exchange}",
            status_code=200,
            text=payload,
        )
        markets = self.cw.markets.list(exchange).markets
        self.assertEqual(exchange, markets[0].exchange)
        self.assertEqual("btceur", markets[0].pair)
        self.assertEqual(True, markets[0].active)

    def test_get_summary(self, requests_mock):
        payload = """
        {
            "result": {
                "price": {
                    "last": 17536.1,
                    "high": 17580.9,
                    "low": 17308.8,
                    "change": {
                        "percentage": 0.007075214352577519,
                        "absolute": 123.0
                    }
                },
                "volume": 456.0,
                "volumeQuote": 50816020.3732981
            },
            "allowance": {
                "cost": 0.005,
                "remaining": 9.969,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/markets/kraken/btcusd/summary",
            status_code=200,
            text=payload,
        )
        market = self.cw.markets.get("kraken:btcusd").market
        self.assertEqual(456.0, market.volume)
        self.assertEqual(123.0, market.price.change_absolute)

    def test_get_ohlc(self, requests_mock):
        payload = """
        {
            "result": {
                "3600": [
                    [1669874400, 17146.7, 17149.8, 17056.8, 17109.8, 114.73225247, 1963044.628486391]

                ],
                "60": [
                    [1673407920, 17410.3, 17410.3, 17409.5, 17409.5, 0.00962118, 167.507430322]
                ]
            },
            "allowance": {
                "cost": 0.015,
                "remaining": 9.924,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/markets/kraken/btcusd/ohlc?periods=60,3600",
            status_code=200,
            text=payload,
        )
        candles = self.cw.markets.get("kraken:btcusd", ohlc=True, periods=["1m", "1h"])
        self.assertEqual(1, len(candles.of_1h))
        self.assertEqual(1669874400, candles.of_1h[0][0])
        self.assertEqual(1, len(candles.of_1m))
        self.assertEqual(1673407920, candles.of_1m[0][0])

    def test_get_trades(self, requests_mock):
        payload = """
        {
            "result": [
                [0, 1673468207, 17541.1, 0.00112469],
                [0, 1673468444, 17553.6, 0.00509578]
            ],
            "allowance": {
                "cost": 0.01,
                "remaining": 9.914,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/markets/kraken/btcusd/trades",
            status_code=200,
            text=payload,
        )
        trades = self.cw.markets.get("kraken:btcusd", trades=True).trades
        self.assertEqual(2, len(trades))
        self.assertEqual(1673468207, trades[0][1])
        self.assertEqual(1673468444, trades[1][1])

    def test_get_orderbook(self, requests_mock):
        payload = """
        {
            "result": {
                "asks": [
                    [17543, 4.52164971],
                    [19668.2, 0.02098424]
                ],
                "bids": [
                    [17542.9, 0.00043966],
                    [16250, 10.26301389]
                ],
                "seqNum": 6044713
            },
            "allowance": {
                "cost": 0.01,
                "remaining": 9.904,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/markets/kraken/btcusd/orderbook",
            status_code=200,
            text=payload,
        )
        orderbook = self.cw.markets.get("kraken:btcusd", orderbook=True)
        self.assertEqual(2, len(orderbook.bids))
        self.assertEqual(17542.9, orderbook.bids[0][0])
        self.assertEqual(0.00043966, orderbook.bids[0][1])

        self.assertEqual(2, len(orderbook.asks))
        self.assertEqual(17543, orderbook.asks[0][0])
        self.assertEqual(4.52164971, orderbook.asks[0][1])

    def test_get_liquidity(self, requests_mock):
        payload = """
        {
            "result": {
                "bid": {
                    "base": {
                        "100": "507.47561712",
                        "150": "533.35849663",
                        "200": "666.23322636",
                        "25": "155.39594935",
                        "250": "676.0338264",
                        "300": "690.29168654",
                        "400": "814.15685701",
                        "50": "384.64395916",
                        "500": "829.73795518",
                        "75": "437.0431331"
                    },
                    "quote": {
                        "100": "8865832.466318421",
                        "150": "9314649.193110492",
                        "200": "11601951.967732011",
                        "25": "2721964.971291948",
                        "250": "11769761.725433515",
                        "300": "12012855.6191805",
                        "400": "14111967.897367644",
                        "50": "6728178.117726981",
                        "500": "14373012.90888131",
                        "75": "7642093.366274467"
                    }
                },
                "ask": {
                    "base": {
                        "100": "476.80955526",
                        "150": "604.82207051",
                        "200": "695.8285238",
                        "25": "132.79209156",
                        "250": "829.04064092",
                        "300": "893.40471551",
                        "400": "961.84571661",
                        "50": "378.14258523",
                        "500": "1022.87115799",
                        "75": "394.89010562"
                    },
                    "quote": {
                        "100": "8395455.931514802",
                        "150": "10668936.649813399",
                        "200": "12293613.23232567",
                        "25": "2331416.305570149",
                        "250": "14681776.134494694",
                        "300": "15840165.777886974",
                        "400": "17083389.166800315",
                        "50": "6650184.641869758",
                        "500": "18204405.813366677",
                        "75": "6945646.21839584"
                    }
                }
            },
            "allowance": {
                "cost": 0.005,
                "remaining": 9.899,
                "upgrade": "For unlimited API access, create an account at https://cryptowat.ch"
            }
        }
        """
        requests_mock.get(
            f"{DEFAULT_REST_ENDPOINT}/markets/kraken/btcusd/orderbook/liquidity",
            status_code=200,
            text=payload,
        )
        liquidity = self.cw.markets.get("kraken:btcusd", liquidity=True).liquidity
        self.assertEqual("507.47561712", liquidity.bid.base["100"])
        self.assertEqual("7642093.366274467", liquidity.bid.quote["75"])
        self.assertEqual("476.80955526", liquidity.ask.base["100"])
        self.assertEqual("6945646.21839584", liquidity.ask.quote["75"])
