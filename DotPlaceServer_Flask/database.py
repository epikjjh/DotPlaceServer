from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import datetimeparser

Base = declarative_base()

class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    path = Column(String(250), nullable=False)
    thumbnail_path = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'path' : self.path,
            'thumbnail_path' : self.thumbnail_path
        }

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)
    name = Column(String(30), nullable=False)
    birthday = Column(String(30), nullable=False)
    gender = Column(Boolean, nullable=False)
    nation = Column(String(30), nullable=False)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'nicknmae' : self.nickname,
            'name' : self.name,
            'birthday' : self.birthday,
            'gender' : self.gender,
            'nation' : self.gender
        }

class Trip(Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    title = Column(String(40))
    #thumbnail_id = Column(Integer, ForeignKey('image.id'))
    owner = Column(Integer, ForeignKey('user.id'))
    owner_index = Column(Integer, nullable=False)   #trip's db id on owner's local machine

    #image = relationship(Image)
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'id' : self.id,
            'title' : self.title,
            #'thumbnail_id' : self.thumbnail_id,
            'owner' : self.owner,
            'image' : self.image,
            'user' : self.user
        }

class Position(Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    time = Column(DateTime, nullable=False)
    type = Column(Integer, nullable=False)
    duration = Column(Integer)
    trip_id = Column(Integer, ForeignKey('trip.id'))

    trip = relationship(Trip)

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'lat' : self.lat,
            'lng' : self.lng,
            'time' : datetimeparser.datetimeToString(self.time),
            'type' : self.type,
            'duration': self.duration,
            'trip_id': self.trip_id
        }

class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    dot_id = Column(Integer, ForeignKey('position.id'))
    time = Column(DateTime, nullable=False)
    thumbnail_id = Column(Integer, ForeignKey('image.id'))

    position = relationship(Position)
    image = relationship(Image)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'dot_id': self.dot_id,
            'time': datetimeparser.datetimeToString(self.time),
            'thumbnail_id': self.thumbnail_id
        }


class ImageInArticle(Base):
    __tablename__ = 'image_in_article'

    image_id = Column(Integer, ForeignKey('image.id'), primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'), primary_key=True)

    image = relationship(Image)
    article = relationship(Article)


engine = create_engine('sqlite:///dotplace.db')
Base.metadata.create_all(engine)

if __name__ == '__main__':
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    guest = User(nickname='Guest', password='p1234')
    session.add(guest)
    session.commit()