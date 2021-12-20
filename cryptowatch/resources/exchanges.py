import datetime as dt
import json
from marshmallow import fields, post_load

from cryptowatch.utils import log
from cryptowatch.resources.allowance import AllowanceSchema
from cryptowatch.resources.base import BaseSchema


class Exchanges:
    def __init__(self, http_client):
        self.client = http_client

    def get(self, exchange):
        log("Getting exchange {}".format(exchange))
        data, http_resp = self.client.get_resource("/exchanges/{}".format(exchange))
        exchange_resp = json.loads(data)
        schema = ExchangeAPIResponseSchema()
        exchange_obj = schema.load(exchange_resp)
        if exchange_obj._allowance:
            log(
                "API Allowance: cost={} remaining={}".format(
                    exchange_obj._allowance.cost, exchange_obj._allowance.remaining
                )
            )
        exchange_obj._http_response = http_resp
        return exchange_obj

    def list(self):
        log("Getting all exchanges")
        data, http_resp = self.client.get_resource("/exchanges")
        exchange_resp = json.loads(data)
        schema = ExchangeListAPIResponseSchema()
        exchanges_obj = schema.load(exchange_resp)
        if exchanges_obj._allowance:
            log(
                "API Allowance: cost={} remaining={}".format(
                    exchanges_obj._allowance.cost, exchanges_obj._allowance.remaining
                )
            )
        exchanges_obj._http_response = http_resp
        return exchanges_obj


class ExchangeResource:
    def __init__(self, id, symbol, name, active, route=None, routes=[]):
        self.id = id
        self.symbol = symbol
        self.name = name
        self.active = active
        if route:
            self.route = route
        if routes:
            self.routes = routes

    def __repr__(self):
        return "<Exchange({self.name})>".format(self=self)


class ExchangeSchema(BaseSchema):
    id = fields.Integer()
    symbol = fields.Str()
    name = fields.Str()
    active = fields.Boolean()
    route = fields.Url()
    routes = fields.Dict(keys=fields.Str(), values=fields.Url())

    @post_load
    def make_exchange(self, data, **kwargs):
        return ExchangeResource(**data)


class ExchangeAPIResponseSchema(BaseSchema):
    result = fields.Nested(ExchangeSchema)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_exchange_api_resp(self, data, **kwargs):
        return ExchangeAPIResponse(**data)


class ExchangeListAPIResponseSchema(BaseSchema):
    result = fields.Nested(ExchangeSchema, many=True)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_exchange_list_api_resp(self, data, **kwargs):
        return ExchangeListAPIResponse(**data)


class ExchangeAPIResponse:
    def __init__(self, result, allowance):
        self.exchange = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<ExchangeAPIResponse({self.exchange})>".format(self=self)


class ExchangeListAPIResponse:
    def __init__(self, result, allowance):
        self.exchanges = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<ExchangeListAPIResponse({self.exchanges})>".format(self=self)
