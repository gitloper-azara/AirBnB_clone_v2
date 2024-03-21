#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship, backref
from os import getenv
from models.review import Review
import models


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'
    city_id = Column(
        String(60),
        ForeignKey('cities.id'),
        nullable=False
    )
    user_id = Column(
        String(60),
        ForeignKey('users.id'),
        nullable=False
    )
    name = Column(
        String(128),
        nullable=False
    )
    description = Column(
        String(1024),
        nullable=True
    )
    number_rooms = Column(
        Integer,
        nullable=False,
        default=0
    )
    number_bathrooms = Column(
        Integer,
        nullable=False,
        default=0
    )
    max_guest = Column(
        Integer,
        nullable=False,
        default=0
    )
    price_by_night = Column(
        Integer,
        nullable=False,
        default=0
    )
    latitude = Column(
        Float,
        nullable=True
    )
    longitude = Column(
        Float,
        nullable=True
    )
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            'Review',
            cascade='all , delete-orphan',
            backref=backref('place', cascade='all')
        )
    # for FileStorage, getter atrribute to return list of City instances
    else:
        @property
        def reviews(self):
            '''Return the list of review instances with place_id equal to
            the current Place.id
            '''
            reviewList = []
            review_instances = models.storage.all(Review)
            for review in review_instances.values():
                if review.place_id == self.id:
                    reviewList.append(review)
            return reviewList
