#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship, backref
from models.city import City
import models
from os import getenv


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(
        String(128),
        nullable=False
    )

    # for DBStorage, relationship with City
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            'City',
            cascade='all, delete, delete-orphan',
            back_populates='state'
        )

    # for FileStorage, getter atrribute to return list of City instances
    else:
        @property
        def cities(self):
            '''Return the list of city instances with state_id equal to
            the current State.id
            '''
            cityList = []
            city_instances = models.storage.all(City)
            for city in city_instances.values():
                if city.state_id == self.id:
                    cityList.append(city)
            return cityList
