from app.api import bp
from flask import request
from app import app
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime

app.config["MONGO_URI"] = "mongodb://localhost:27017/news_portal_db"
mongo = PyMongo(app)


@bp.route("/authors", methods=["GET"])
def get_all_authors():
    authors = mongo.db.authors.find({})
    return dumps(authors, ensure_ascii=False)


@bp.route("/authors/search", methods=["GET"])
def search_authors():
    search = request.args.get("search")
    authors = mongo.db.authors.find(
        {
            "$or": [
                {"_id": ObjectId(search)},
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
            ]
        }
    )

    return dumps(authors, ensure_ascii=False)


@bp.route("/authors", methods=["POST"])
def create_author():
    request_body = request.json
    if ("name" in request_body) and ("email" in request_body):
        if (request_body["name"] != "") and (request_body["email"] != ""):
            request_body["created_on"] = datetime.utcnow()
            status = mongo.db.authors.insert_one(request_body)
            return str(status.inserted_id)
        else:
            return "These fields cannot be empty: name and email"
    else:
        return "These fields are required: name and email"


@bp.route("/authors", methods=["PATCH"])
def update_author():
    request_body = request.json
    document_to_update = request.args.get("document_to_update")
    status = mongo.db.authors.update(
        {"_id": ObjectId(document_to_update)}, request_body
    )

    return status


@bp.route("/authors", methods=["DELETE"])
def remove_author():
    document_to_remove = request.args.get("document_to_remove")
    status = mongo.db.authors.remove({"_id": ObjectId(document_to_remove)})

    return status
