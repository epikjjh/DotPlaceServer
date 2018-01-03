from flask import Blueprint, jsonify
json_blueprint = Blueprint('json_blueprint', __name__)

from database import Image, User, Trip, Position, Article

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///dotplace.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

@json_blueprint.route('/user/json')
def UserJson():
    users = session.query(User).all()
    return jsonify(Users=[u.serialize for u in users])

@json_blueprint.route('/article/json')
def ArticleJson():
    articles = session.query(Article).order_by(desc(Article.time)).all()
    return jsonify(Articles=[a.serialize for a in articles])
