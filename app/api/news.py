from app.api import bp
from flask import request
from app import app
from flask_pymongo import PyMongo
from bson.json_util import dumps
from datetime import datetime

# datetime.datetime.utcnow()


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
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"authors": {"$regex": search, "$options": "i"}},
            ]
        }
    )

    return dumps(posts, ensure_ascii=False)


@bp.route("/news", methods=["POST"])
def create_news():
    pass


@bp.route("/news/<int:id>", methods=["PATCH"])
def update_news(id):
    pass


@bp.route("/news", methods=["DELETE"])
def remove_news():
    pass
