import datetime as dt
import json
from marshmallow import fields, post_load

from cryptowatch.utils import log
from cryptowatch.resources.allowance import AllowanceSchema
from cryptowatch.resources.assets import AssetSchema
from cryptowatch.resources.base import BaseSchema
from cryptowatch.resources.markets import MarketSchema


class Instruments:
    def __init__(self, http_client):
        self.client = http_client

    def get(self, instrument):
        log("Getting instrument {}".format(instrument))
        data, http_resp = self.client.get_resource("/pairs/{}".format(instrument))
        instrument_resp = json.loads(data)
        schema = InstrumentAPIResponseSchema()
        instrument_obj = schema.load(instrument_resp)
        if instrument_obj._allowance:
            log(
                "API Allowance: cost={} remaining={}".format(
                    instrument_obj._allowance.cost, instrument_obj._allowance.remaining
                )
            )
        instrument_obj._http_response = http_resp
        return instrument_obj

    def list(self):
        log("Getting instruments")
        data, http_resp = self.client.get_resource("/pairs")
        instrument_resp = json.loads(data)
        schema = InstrumentListAPIResponseSchema()
        instruments_obj = schema.load(instrument_resp)
        if instruments_obj._allowance:
            log(
                "API Allowance: cost={} remaining={}".format(
                    instruments_obj._allowance.cost,
                    instruments_obj._allowance.remaining,
                )
            )
        instruments_obj._http_response = http_resp
        return instruments_obj


class InstrumentResource:
    def __init__(
        self, id, symbol, route, base, quote, futuresContractPeriod=None, markets=[]
    ):
        self.id = id
        self.symbol = symbol
        self.route = route
        self.base = base
        self.quote = quote
        if futuresContractPeriod:
            self.futures_contract_period = futuresContractPeriod
        if markets:
            self.markets = markets

    def __repr__(self):
        return "<Instrument({self.symbol})>".format(self=self)


class InstrumentSchema(BaseSchema):
    id = fields.Integer()
    symbol = fields.Str()
    route = fields.Url()
    base = fields.Nested(AssetSchema)
    quote = fields.Nested(AssetSchema)
    futuresContractPeriod = fields.Str()
    markets = fields.Nested(MarketSchema, many=True)

    @post_load
    def make_instruments(self, data, **kwargs):
        return InstrumentResource(**data)


class InstrumentAPIResponseSchema(BaseSchema):
    result = fields.Nested(InstrumentSchema)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_instrument_api_resp(self, data, **kwargs):
        return InstrumentAPIResponse(**data)


class InstrumentListAPIResponseSchema(BaseSchema):
    result = fields.Nested(InstrumentSchema, many=True)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_instrument_list_api_resp(self, data, **kwargs):
        return InstrumentListAPIResponse(**data)


class InstrumentAPIResponse:
    def __init__(self, result, allowance):
        self.instrument = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<InstrumentAPIResponse({self.instrument})>".format(self=self)


class InstrumentListAPIResponse:
    def __init__(self, result, allowance):
        self.instruments = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<InstrumentListAPIResponse({self.instruments})>".format(self=self)
