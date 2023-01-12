import datetime as dt
import json
from marshmallow import fields, post_load

from cryptowatch.utils import log, validate_limit
from cryptowatch.resources.allowance import AllowanceSchema
from cryptowatch.resources.base import BaseResource, BaseSchema
from cryptowatch.resources.markets import MarketSchema


class Assets:
    MAX_LIMIT = 5000

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

    def list(self, limit=None):
        query = {}

        log("Listing all assets")

        if limit:
            validate_limit(limit, self.MAX_LIMIT)
            query["limit"] = limit

        data, http_resp = self.client.get_resource("/assets", query=query)
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
    def make_resource(self, data, **kwargs):
        return BaseResource(_name="Asset", _display_key="name", **data)


class AssetAPIResponseSchema(BaseSchema):
    result = fields.Nested(AssetSchema)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), load_default=None)

    @post_load
    def make_asset(self, data, **kwargs):
        return AssetAPIResponse(**data)


class AssetListAPIResponseSchema(BaseSchema):
    result = fields.Nested(AssetSchema, many=True)
    allowance = fields.Nested(AllowanceSchema, partial=("account",), load_default=None)

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
