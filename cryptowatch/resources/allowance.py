from marshmallow import fields, post_load

from cryptowatch.resources.base import BaseSchema


class AllowanceSchema(BaseSchema):
    cost = fields.Integer()
    remaining = fields.Integer()
    remainingPaid = fields.Integer(missing=0)
    upgrade = fields.Str(missing="")
    account = fields.Str(missing="")

    @post_load
    def make_allowance(self, data, **kwargs):
        return AllowanceResource(**data)


class AllowanceResource:
    def __init__(self, cost, remaining, remainingPaid=0, upgrade="", account=""):
        self.cost = cost
        self.remaining = remaining
        self.remaining_paid = remainingPaid
        self.upgrade = upgrade
        if account:
            self.account = account

    def __repr__(self):
        return "<Allowance({self.remaining})>".format(self=self)
