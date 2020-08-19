from app.api import bp
from flask import request
from app import app
from flask_pymongo import PyMongo
from bson.json_util import dumps

app.config["MONGO_URI"] = "mongodb://localhost:27017/news_portal_db"
mongo = PyMongo(app)


@bp.route("/authors", methods=["GET"])
def get_all_authors():
    authors = mongo.db.authors.find({})
    return dumps(authors, ensure_ascii=False)


@bp.route("/news/search", methods=["GET"])
def search_authors():
    pass


@bp.route("/news", methods=["POST"])
def create_author():
    pass


@bp.route("/news/<int:id>", methods=["PATCH"])
def update_author(id):
    pass


@bp.route("/news", methods=["DELETE"])
def remove_author():
    pass
