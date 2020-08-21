from app.api import bp
from flask import request
from app import app
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime


app.config["MONGO_URI"] = "mongodb://localhost:27017/news_portal_db"
mongo = PyMongo(app)


@bp.route("/news/", methods=["GET"])
def get_all_news():
    posts = mongo.db.posts.find({})
    return dumps(posts, ensure_ascii=False)


@bp.route("/news/search", methods=["GET"])
def search_news():
    search = request.args.get("search")
    posts = mongo.db.posts.find(
        {
            "$or": [
                {"_id": ObjectId(search)},
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"authors": {"$regex": search, "$options": "i"}},
            ]
        }
    )

    return dumps(posts, ensure_ascii=False)


@bp.route("/news", methods=["POST"])
def create_news():
    request_body = request.json
    if (
        ("title" in request_body)
        and ("content" in request_body)
        and ("authors" in request_body)
    ):
        if (
            (request_body["title"] != "")
            and (request_body["content"] != "")
            and (request_body["authors"] != "")
        ):
            request_body["created_on"] = datetime.utcnow()
            status = mongo.db.posts.insert_one(request_body)
            return str(status.inserted_id)
        else:
            return "These fields cannot be empty: title, content and authors"
    else:
        return "These fields are required: title, content and authors"


@bp.route("/news", methods=["PATCH"])
def update_news():
    request_body = request.json
    document_to_update = request.args.get("document_to_update")
    status = mongo.db.posts.update({"_id": ObjectId(document_to_update)}, request_body)

    return status


@bp.route("/news", methods=["DELETE"])
def remove_news():
    document_to_remove = request.args.get("document_to_remove")
    status = mongo.db.posts.remove({"_id": ObjectId(document_to_remove)})

    return status
