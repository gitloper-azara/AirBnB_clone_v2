#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(
        String(60),
        nullable=False,
        primary_key=True
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now()
    )

    def __init__(self, *args, **kwargs) -> None:
        """An instance of BaseModel class

        Args:
            *args (any): variable arguments.
            **kwargs (any): key-worded arguments.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%S.%f'
                            )
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = self.created_at
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        dictionary = dict(self.__dict__)
        dictionary.pop('_sa_instance_state', None)
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(
            cls, self.id, self.dict_without_sa_instance()
            )

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def dict_without_sa_instance(self):
        '''delete _sa_instance_state from dict'''
        dictionary = dict(self.__dict__)
        # remove _sa_instance_state here, if it exits
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.dict_without_sa_instance()
        dictionary.update({'__class__': self.__class__.__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        '''Deletes the current instance from the storage'''
        models.storage.delete(self)
