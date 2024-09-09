from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import EventModel
from schemas import EventSchema


blp = Blueprint("Events", __name__, description="Operations on events")


@blp.route("/event/<string:event_id>")
class Event(MethodView):
    @blp.response(200, EventSchema)
    def get(cls, event_id):
        event = EventModel.query.get_or_404(event_id)
        return event

    def delete(cls, event_id):
        event = EventModel.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}


@blp.route("/event")
class EventList(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(cls):
        return EventModel.query.all()

    @blp.arguments(EventSchema)
    @blp.response(201, EventSchema)
    def post(self, event_data):
        event = EventModel(**event_data)

        try:
            db.session.add(event)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An Event with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the rsvp.")

        return event