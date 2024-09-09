from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    event = db.relationship("EventModel", back_populates="tags")
    rsvps = db.relationship("RsvpModel", back_populates="tags", secondary="rsvps_tags")