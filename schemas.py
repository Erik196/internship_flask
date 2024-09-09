from marshmallow import Schema, fields

class PlainRsvpSchema(Schema):
    id = fields.Int(dump_only=True)
    response = fields.Str(required=True)

class PlainEventSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date = fields.Str(required=True)
    organiser = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class RsvpUpdateSchema(Schema):
    response = fields.Str(required=True) 

class RsvpSchema(PlainRsvpSchema):
    event_id = fields.Int(required=True, load_only=True)
    event = fields.Nested(PlainEventSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class EventSchema(PlainEventSchema):
    rsvps = fields.List(fields.Nested(PlainRsvpSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    event_id = fields.Int(load_only=True)
    event = fields.Nested(PlainEventSchema(), dump_only=True)
    rsvps = fields.List(fields.Nested(PlainRsvpSchema()), dump_only=True)

class TagAndRsvpSchema(Schema):
    message = fields.Str()
    rsvp = fields.Nested(RsvpSchema)
    tag = fields.Nested(TagSchema)

class TagAndEventSchema(Schema):
    message = fields.Str()
    event = fields.Nested(EventSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)