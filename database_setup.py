from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

db = SQLAlchemy()

Base = declarative_base()


class User(UserMixin, db.Model, Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    flights = relationship("FlightTrack", back_populates='user')



class FlightTrack(db.Model, Base):
    __tablename__ = 'tracking'
    id = db.Column(db.Integer, primary_key=True)
    departing = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", back_populates='flights')
