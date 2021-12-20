from marshmallow import EXCLUDE, Schema


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
