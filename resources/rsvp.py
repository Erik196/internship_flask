from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import RsvpModel
from schemas import RsvpSchema, RsvpUpdateSchema

blp = Blueprint("Rsvps", __name__, description="Operations on rsvps")


@blp.route("/rsvp/<string:rsvp_id>")
class Rsvp(MethodView):
    @jwt_required()
    @blp.response(200, RsvpSchema)
    def get(self, rsvp_id):
        rsvp = RsvpModel.query.get_or_404(rsvp_id)
        return rsvp

    @jwt_required()
    def delete(self, rsvp_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        rsvp = RsvpModel.query.get_or_404(rsvp_id)
        db.session.delete(rsvp)
        db.session.commit()
        return {"message": "Rsvp deleted."}

    @blp.arguments(RsvpUpdateSchema)
    @blp.response(200, RsvpSchema)
    def put(self, rsvp_data, rsvp_id):
        rsvp = RsvpModel.query.get_or_404(rsvp_id)

        if rsvp:
            rsvp.response = rsvp_data["response"]
        else:
            rsvp = RsvpModel(**rsvp_data)

        db.session.add(rsvp)
        db.session.commit()

        return rsvp


@blp.route("/rsvp")
class RsvpList(MethodView):
    @jwt_required()
    @blp.response(200, RsvpSchema(many=True))
    def get(self):
        return RsvpModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(RsvpSchema)
    @blp.response(201, RsvpSchema)
    def post(self, rsvp_data):
        rsvp = RsvpModel(**rsvp_data)

        try:
            db.session.add(rsvp)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the rsvp.")

        return rsvp