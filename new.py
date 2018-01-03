from flask import Blueprint, render_template, request

new_blueprint = Blueprint('new_blueprint', __name__)

UPLOAD_FOLDER = './images/'
THUMBNAIL_SIZE = (800, 600)

from database import Image, User, Trip, Position, Article, ImageInArticle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///dotplace.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

import datetime
import datetimeparser
import urllib
import PIL.Image


@new_blueprint.route('/user/new', methods=['POST'])
def NewUser():
    nickname = request.form['nickname']
    password = request.form['password']
    print('signup request ' + nickname + ' ' + password)
    user = User(nickname=nickname, password=password)
    session.add(user)
    session.commit()

    return str(user.id), str(301)


@new_blueprint.route('/trip/id/<owner>/<owner_index>')
def TripId(owner, owner_index):
    trip = session.query(Trip).filter_by(owner=owner, owner_index=owner_index).first()
    if trip == None:
        return '0'
    return str(trip.id)


@new_blueprint.route('/trip/new', methods=['POST'])
def NewTrip():
    title = urllib.parse.unquote_plus(request.form['title'])
    owner = int(request.form['owner'])
    owner_index = int(request.form['owner_index'])
    count = int(request.form['count'])

    # Inser duplicate check here

    trip = Trip(title=title, owner=owner, owner_index=owner_index)
    session.add(trip)
    session.flush()

    for i in range(count):
        pContent = request.form['position' + str(i)].split()
        pTime = datetimeparser.parseDatetime(request.form['position' + str(i) + '_time'])
        p = Position(lat=pContent[0], lng=pContent[1], type=pContent[2], duration=pContent[3], trip_id=trip.id,
                     time=pTime)
        session.add(p)
        session.flush()

    session.commit()

    print('inserted trip ' + str(trip.id))

    return str(trip.id), str(301)


@new_blueprint.route('/article/new', methods=['POST'])
def NewArticle():
    print('POST article')
    content = urllib.parse.unquote_plus(request.form['content'])
    trip_id = int(request.form['trip_id'])
    position_index = int(request.form['dot_index'])
    thumbnail_index = int(request.form['thumbnail_index'])
    count = int(request.form['count'])

    # Find the dot writing to
    positions = session.query(Position).filter_by(trip_id=trip_id).order_by(Position.time).all()
    position = positions[position_index]

    # Insert article into DB
    article = Article(content=content, dot_id=position.id, time=datetime.datetime.now())
    session.add(article)
    session.flush()

    # Insert images
    for i in range(count):
        file = request.files['image' + str(i)]

        newImage = Image(path='', thumbnail_path='')
        session.add(newImage)
        session.flush()

        newId = newImage.id

        newImage.path = str(newId) + '.jpeg'
        file.save(UPLOAD_FOLDER + newImage.path)

        newImage.thumbnail_path = UPLOAD_FOLDER + str(newId) + '.thumbnail.jpeg'
        im = PIL.Image.open(UPLOAD_FOLDER + newImage.path)
        im.thumbnail(THUMBNAIL_SIZE)
        im.save(newImage.thumbnail_path)

        session.add(newImage)
        session.flush()

        newIiA = ImageInArticle(image_id=newId, article_id=article.id)
        session.add(newIiA)
        session.flush()

        if i == thumbnail_index:
            article.thumbnail_id = newId
            session.add(article)
            session.flush()
        print('\timage ' + str(newId) + ' written')

    session.commit()
    print('Inserted article ' + str(article.id))
    return str(article.id), str(301)
