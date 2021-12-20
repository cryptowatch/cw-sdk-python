import datetime as dt
import json
from marshmallow import fields, post_load

from cryptowatch.utils import log, translate_periods
from cryptowatch.resources.allowance import AllowanceSchema
from cryptowatch.resources.base import BaseSchema


class Markets:
    def __init__(self, http_client):
        self.client = http_client

    def get(
        self,
        market,
        liquidity=False,
        orderbook=False,
        trades=False,
        ohlc=False,
        periods=[],
    ):
        exchange, pair = market.split(":")
        if ohlc:
            log("Getting market OHLC candles {}".format(market))
            resource = "/markets/{}/{}/ohlc".format(exchange, pair)
            if periods:
                sec_periods = translate_periods(periods)
                resource += "?periods={}".format(",".join(sec_periods))
            schema = MarketOHLCAPIResponseSchema()
        elif trades:
            log("Getting market trades {}".format(market))
            resource = "/markets/{}/{}/trades".format(exchange, pair)
            schema = MarketTradesAPIResponseSchema()
        elif orderbook:
            log("Getting market orderbook {}".format(market))
            resource = "/markets/{}/{}/orderbook".format(exchange, pair)
            schema = MarketOrderBookAPIResponseSchema()
        elif liquidity:
            log("Getting market liquidity {}".format(market))
            resource = "/markets/{}/{}/orderbook/liquidity".format(exchange, pair)
            schema = MarketLiquidityAPIResponseSchema()
        else:
            log("Getting market summary {}".format(market))
            resource = "/markets/{}/{}/summary".format(exchange, pair)
            schema = MarketSummaryAPIResponseSchema()
        data, http_resp = self.client.get_resource(resource)
        market_resp = json.loads(data)
        market_obj = schema.load(market_resp)
        if market_obj._allowance:
            log(
                "API Allowance: cost={} remaining={}".format(
                    market_obj._allowance.cost, market_obj._allowance.remaining
                )
            )
        market_obj._http_response = http_resp
        return market_obj

    def list(self, exchange=None):
        if exchange:
            resource = "/markets/{}".format(exchange)
            log("Getting all markets for {}".format(exchange))
        else:
            resource = "/markets"
            log("Getting all markets for all exchanges")
        data, http_resp = self.client.get_resource(resource)
        market_resp = json.loads(data)
        schema = MarketListAPIResponseSchema()
        markets_obj = schema.load(market_resp)
        if markets_obj._allowance:
            log(
                "API Allowance: cost={} remaining={}".format(
                    markets_obj._allowance.cost, markets_obj._allowance.remaining
                )
            )
        markets_obj._http_response = http_resp
        return markets_obj


class MarketResource:
    def __init__(self, id, exchange, pair, active, route=None, routes=[]):
        self.id = id
        self.exchange = exchange
        self.pair = pair
        self.active = active
        if route:
            self.route = route
        if routes:
            self.routes = routes

    def __repr__(self):
        return "<Market({self.exchange}:{self.pair})>".format(self=self)


class MarketSchema(BaseSchema):

    id = fields.Integer()
    exchange = fields.Str()
    pair = fields.Str()
    active = fields.Boolean()
    route = fields.Url()
    routes = fields.Dict(keys=fields.Str(), values=fields.Url())

    @post_load
    def make_market(self, data, **kwargs):
        return MarketResource(**data)


class MarketSummaryResource:
    def __init__(self, price, volume, volumeQuote):
        self.price = price
        self.volume = volume
        self.volume_quote = volumeQuote

    def __repr__(self):
        return "<MarketSummary({self.price})>".format(self=self)


class MarketSummaryPriceSchema(BaseSchema):

    change = fields.Dict(keys=fields.Str(), values=fields.Float())
    last = fields.Float()
    high = fields.Float()
    low = fields.Float()

    @post_load
    def make_market_summary_price(self, data, **kwargs):
        return MarketSummaryPriceResource(**data)


class MarketSummaryPriceResource:
    def __init__(self, last, high, low, change):
        self.last = last
        self.high = high
        self.low = low
        self.change = change.get("percentage")
        self.change_absolute = change.get("absolute")

    def __repr__(self):
        return "<MarketSummaryPriceResource({self.last})>".format(self=self)


class MarketSummarySchema(BaseSchema):

    price = fields.Nested(MarketSummaryPriceSchema)
    volume = fields.Float()
    volumeQuote = fields.Float()

    @post_load
    def make_market_summary(self, data, **kwargs):
        return MarketSummaryResource(**data)


class LiquidityLevelSchema(BaseSchema):
    base = fields.Dict(keys=fields.Str(), values=fields.Str())
    quote = fields.Dict(keys=fields.Str(), values=fields.Str())

    @post_load
    def make_liquidity_level(self, data, **kwargs):
        return LiquidityLevelResource(**data)


class LiquidityLevelResource:
    def __init__(self, quote, base):
        self.quote = quote
        self.base = base


class LiquiditySchema(BaseSchema):
    bid = fields.Nested(LiquidityLevelSchema)
    ask = fields.Nested(LiquidityLevelSchema)

    @post_load
    def make_liquidity(self, data, **kwargs):
        return LiquidityResource(**data)


class LiquidityResource:
    def __init__(self, bid, ask):
        self.bid = bid
        self.ask = ask


class MarketLiquidityAPIResponseSchema(BaseSchema):
    result = fields.Nested(LiquiditySchema)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_market_liquidity_api_resp(self, data, **kwargs):
        return MarketLiquidityAPIResponse(**data)


class MarketLiquidityAPIResponse:
    def __init__(self, result, allowance):
        self.liquidity = result
        self._allowance = allowance

    def __repr__(self):
        return "<MarketLiquidityAPIResponse()>"


class OrdeBookSchema(BaseSchema):
    bids = fields.List(fields.List(fields.Float))
    asks = fields.List(fields.List(fields.Float))
    seqNum = fields.Integer()


class MarketOrderBookAPIResponseSchema(BaseSchema):
    result = fields.Nested(OrdeBookSchema)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_market_order_book_api_resp(self, data, **kwargs):
        return MarketOrderBookAPIResponse(**data)


class MarketOrderBookAPIResponse:
    def __init__(self, result, allowance):
        self.bids = result.get("bids")
        self.asks = result.get("asks")
        self._legend = ["price", "amount"]
        self._allowance = allowance

    def __repr__(self):
        return "<MarketOrderBookAPIResponse()>"


class MarketTradesAPIResponseSchema(BaseSchema):
    result = fields.List(fields.List(fields.Float))
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_market_trade_api_resp(self, data, **kwargs):
        return MarketTradesAPIResponse(**data)


class MarketTradesAPIResponse:
    def __init__(self, result, allowance):
        self.trades = result
        self._legend = ["id", "timestamp", "price", "amount"]
        self._allowance = allowance

    def __repr__(self):
        return "<MarketTradeAPIResponse({self.trades})>".format(self=self)


class MarketOHLCAPIResponseSchema(BaseSchema):
    result = fields.Dict(fields.Str(), fields.List(fields.List(fields.Float)))
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_market_ohlc_api_resp(self, data, **kwargs):
        return MarketOHLCAPIResponse(**data)


class MarketOHLCAPIResponse:
    def __init__(self, result, allowance):
        if result.get("60", []):
            self.of_1m = result.get("60", [])
        if result.get("180", []):
            self.of_3m = result.get("180", [])
        if result.get("300", []):
            self.of_5m = result.get("300", [])
        if result.get("900", []):
            self.of_15m = result.get("900", [])
        if result.get("1800", []):
            self.of_30m = result.get("1800", [])
        if result.get("3600", []):
            self.of_1h = result.get("3600", [])
        if result.get("7200", []):
            self.of_2h = result.get("7200", [])
        if result.get("14400", []):
            self.of_4h = result.get("14400", [])
        if result.get("21600", []):
            self.of_6h = result.get("21600", [])
        if result.get("43200", []):
            self.of_12h = result.get("43200", [])
        if result.get("86400", []):
            self.of_1d = result.get("86400", [])
        if result.get("259200", []):
            self.of_3d = result.get("259200", [])
        if result.get("604800", []):
            self.of_1w = result.get("604800", [])
        if result.get("604800_Monday", []):
            self.of_1w_monday = result.get("604800_Monday", [])
        self._legend = [
            "close timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume base",
            "volume quote",
        ]
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<MarketOHLCAPIResponse()>"


class MarketSummaryAPIResponseSchema(BaseSchema):
    result = fields.Nested(MarketSummarySchema)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_market_summary_api_resp(self, data, **kwargs):
        return MarketSummaryAPIResponse(**data)


class MarketSummaryAPIResponse:
    def __init__(self, result, allowance):
        self.market = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<MarketSummaryAPIResponse({self.market})>".format(self=self)


class MarketAPIResponse:
    def __init__(self, result, allowance):
        self.market = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<MarketAPIResponse({self.market})>".format(self=self)


class MarketAPIResponseSchema(BaseSchema):
    result = fields.Nested(MarketSchema)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_market_api_resp(self, data, **kwargs):
        return MarketAPIResponse(**data)


class MarketListAPIResponseSchema(BaseSchema):
    result = fields.Nested(MarketSchema, many=True)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_market_api_resp(self, data, **kwargs):
        return MarketListAPIResponse(**data)


class MarketListAPIResponse:
    def __init__(self, result, allowance):
        self.markets = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<MarketAPIResponse({self.markets})>".format(self=self)
