from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, EventModel, RsvpModel
from schemas import TagSchema, TagAndRsvpSchema, TagAndEventSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/event/<string:event_id>/tag")
class TagsInEvent(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, event_id):
        event = EventModel.query.get_or_404(event_id)

        return event.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, event_id):
        tag = TagModel(**tag_data, event_id=event_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag


@blp.route("/rsvp/<string:rsvp_id>/tag/<string:tag_id>")
class LinkTagsToRsvp(MethodView):
    @blp.response(201, TagSchema)
    def post(self, rsvp_id, tag_id):
        rsvp = RsvpModel.query.get_or_404(rsvp_id)
        tag = TagModel.query.get_or_404(tag_id)

        rsvp.tags.append(tag)

        try:
            db.session.add(rsvp)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndRsvpSchema)
    def delete(self, rsvp_id, tag_id):
        rsvp = RsvpModel.query.get_or_404(rsvp_id)
        tag = TagModel.query.get_or_404(tag_id)

        rsvp.tags.remove(tag)

        try:
            db.session.add(rsvp)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Rsvp removed from tag", "rsvp": rsvp, "tag": tag}