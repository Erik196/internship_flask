from db import db



class RsvpTags(db.Model):
    __tablename__ = "rsvps_tags"

    id = db.Column(db.Integer, primary_key=True)
    rsvp_id = db.Column(db.Integer, db.ForeignKey("rsvps.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    
class RsvpModel(db.Model):
    __tablename__ = "rsvps"

    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(50), nullable = False)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), unique=False, nullable=False)
    event = db.relationship("EventModel", back_populates="rsvps")
    tags = db.relationship("TagModel", back_populates="rsvps", secondary="rsvps_tags")
