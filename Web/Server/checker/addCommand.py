from marshmallow import Schema, fields

class AddCommandSchema(Schema):
    description = fields.String(required=True)
    file = fields.String(required=True)
    data = fields.Dict(required=False)