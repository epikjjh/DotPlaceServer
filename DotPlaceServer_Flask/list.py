from flask import Blueprint, render_template
list_blueprint = Blueprint('list_blueprint', __name__)

from database import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///dotplace.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

@list_blueprint.route('/user')
def UserList():
	users = session.query(User).all()
	return render_template('userlist.html', users=users)

@list_blueprint.route('/trip')
def TripList():
	trips = session.query(Trip).all()
	return render_template('triplist.html', trips=trips)

@list_blueprint.route('/position/<int:trip_id>')
def PositionList(trip_id):
	trip = session.query(Trip).filter_by(id=trip_id)
	positions = session.query(Position).filter_by(trip_id=trip_id)
	return render_template('positionlist.html', trip=trip, positions=positions)

@list_blueprint.route('/article')
def ArticleList():
	articles = session.query(Article).all()
	return render_template('articlelist.html', articles=articles)
