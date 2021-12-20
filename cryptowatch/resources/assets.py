import datetime as dt
import json
from marshmallow import fields, post_load

from cryptowatch.utils import log
from cryptowatch.resources.allowance import AllowanceSchema
from cryptowatch.resources.base import BaseSchema
from cryptowatch.resources.markets import MarketSchema


class Assets:
    def __init__(self, http_client):
        self.client = http_client

    def get(self, asset):
        log("Getting asset {}".format(asset))
        data, http_resp = self.client.get_resource("/assets/{}".format(asset))
        asset_resp = json.loads(data)
        schema = AssetAPIResponseSchema()
        asset_obj = schema.load(asset_resp)
        if asset_obj._allowance:
            log(
                "API Allowance: cost={} remaining={}".format(
                    asset_obj._allowance.cost, asset_obj._allowance.remaining
                )
            )
        asset_obj._http_response = http_resp
        return asset_obj

    def list(self):
        log("Listing all assets")
        data, http_resp = self.client.get_resource("/assets")
        asset_resp = json.loads(data)
        schema = AssetListAPIResponseSchema()
        assets_obj = schema.load(asset_resp)
        if assets_obj._allowance:
            log(
                "API Allowance: cost={} remaining={}".format(
                    assets_obj._allowance.cost, assets_obj._allowance.remaining
                )
            )
        assets_obj._http_response = http_resp
        return assets_obj


class AssetResource:
    def __init__(self, id, symbol, name, fiat, markets=None, route=None):
        self.id = id
        self.symbol = symbol
        self.name = name
        self.fiat = fiat
        if markets:
            self.markets = markets
        if route:
            self.route = route

    def __repr__(self):
        return "<Asset({self.name})>".format(self=self)


class AssetSchema(BaseSchema):
    id = fields.Integer()
    symbol = fields.Str()
    name = fields.Str()
    fiat = fields.Boolean()
    route = fields.Url()
    markets = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MarketSchema, many=True)
    )

    @post_load
    def make_asset(self, data, **kwargs):
        return AssetResource(**data)


class AssetAPIResponseSchema(BaseSchema):
    result = fields.Nested(AssetSchema)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_asset(self, data, **kwargs):
        return AssetAPIResponse(**data)


class AssetListAPIResponseSchema(BaseSchema):
    result = fields.Nested(AssetSchema, many=True)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), missing=None)

    @post_load
    def make_asset(self, data, **kwargs):
        return AssetListAPIResponse(**data)


class AssetAPIResponse:
    def __init__(self, result, allowance):
        self.asset = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<AssetAPIResponse({self.asset})>".format(self=self)


class AssetListAPIResponse:
    def __init__(self, result, allowance):
        self.assets = result
        self._allowance = allowance
        self._fetched_at = dt.datetime.now()

    def __repr__(self):
        return "<AssetListAPIResponse({self.assets})>".format(self=self)
