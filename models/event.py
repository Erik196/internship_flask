from db import db

class EventModel(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    date = db.Column(db.String(10), nullable = False)
    organiser = db.Column(db.String(80), nullable = False)

    rsvps = db.relationship("RsvpModel", back_populates="event", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates = "event", lazy = "dynamic")