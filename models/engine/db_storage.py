#!/usr/bin/python3

from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from os import getenv


class DBStorage:
    '''New database storage engine'''

    __engine = None
    __session = None
    __classes = [State, City, User, Place]

    def __init__(self) -> None:
        '''instantiates the DBStorage obj'''
        db_url = (
            f"mysql+mysqldb://{getenv('HBNB_MYSQL_USER')}:"
            f"{getenv('HBNB_MYSQL_PWD')}@{getenv('HBNB_MYSQL_HOST')}"
            f"/{getenv('HBNB_MYSQL_DB')}"
        )
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        # drop all tables if env variable 'HBNB_ENV' == 'test'
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''query all objects on the current database session, depending
        of the class name
        '''
        objects = {}

        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for clss in self.__classes:
                for obj in self.__session.query(clss):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj

        return objects

    def new(self, obj):
        '''add the object to the current database session'''
        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current database session'''
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        '''create all tables in the database in the current session'''
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)()

    def close(self):
        '''close the current database session'''
        self.__session.close()
