from marshmallow import Schema, fields


class CreateSchema(Schema):
    user = fields.Str(required=True)
    institution = fields.Int(required=True)
    content = fields.Dict(required=True)
    module = fields.Str(required=True)
    available = fields.Bool(required=True)

class PromptSchema(Schema):
    prompt = fields.Str(required=True)
    chat_history = fields.Dict(required=False)