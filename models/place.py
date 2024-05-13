#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship, backref
from os import getenv
from models.review import Review
from models.amenity import Amenity
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

    cities = relationship(
        'City',
        back_populates='places'
    )
    user = relationship(
        'User',
        back_populates='places'
    )

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            'Review',
            cascade='all, delete-orphan',
            back_populates='place'
        )
        amenities = relationship(
            'Amenity',
            secondary='place_amenity',
            viewonly=False,
            back_populates='places'
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

        @property
        def amenities(self):
            '''Return the list of amenity instances based on the attr
            amenity_ids that contains Amenity.id linked to the Place
            '''
            amenityList = []
            amenity_instances = models.storage.all(Amenity)
            for amenity in amenity_instances.values():
                if amenity.id in self.amenity_ids:
                    amenityList.append(amenity)
            return amenityList

        @amenities.setter
        def amenities(self, object):
            '''handles append method for adding an Amenity.id to the
            attr amenity_ids
            '''
            if isinstance(object, Amenity):
                self.amenity_ids.append(object.id)

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        primary_key=True,
        nullable=False
    ),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        primary_key=True,
        nullable=False
    )
)
