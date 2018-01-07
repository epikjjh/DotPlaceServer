from flask import Blueprint, render_template, request, send_from_directory

image_blueprint = Blueprint('image_blueprint', __name__)

UPLOAD_FOLDER = './images/'

from database import Image

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///dotplace.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

import os


@image_blueprint.route('/image', methods=['GET', 'POST'])
def Images():
    if request.method == 'POST':
        result = ''
        print('POST request')
        for key in request.files.keys():
            file = request.files[key]

            newImage = Image(path='', thumbnail_path='')
            session.add(newImage)
            session.flush()

            newId = newImage.id

            newImage.path = str(newId) + '.jpeg'
            file.save(UPLOAD_FOLDER + newImage.path)
            session.add(newImage)
            session.flush()

            result += ' ' + str(newId)
        session.commit()
        return result, str(301)

    else:
        images = session.query(Image).all()
        return render_template('imagelist.html', imageCount=len(images), images=images)


@image_blueprint.route('/image/<imageId>')
def GetImage(imageId):
    image = session.query(Image).filter_by(id=imageId).first()
    return send_from_directory(UPLOAD_FOLDER, imageId + '.jpeg')