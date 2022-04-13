#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from os import getenv
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    # if getenv("HBNB_TYPE_STORAGE") == "db":
    id = Column(
        String(60),
        nullable=False,
        primary_key=True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow(),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow(),
        nullable=False
    )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            # if kwargs doesn't contain an id add it
            if not "id" in kwargs:
                kwargs["id"] = str(uuid.uuid4())

            # if kwargs doesn't contain an updated_at add it
            if not "updated_at" in kwargs:
                kwargs["updated_at"] = datetime.now()
            else:
                kwargs["updated_at"] = datetime.strptime(
                    kwargs['updated_at'],
                    '%Y-%m-%dT%H:%M:%S.%f'
                )

            # if kwargs doesn't contain a created_at add it
            if not "created_at" in kwargs:
                kwargs["created_at"] = datetime.now()
            else:
                kwargs["created_at"] = datetime.strptime(
                    kwargs['created_at'],
                    '%Y-%m-%dT%H:%M:%S.%f'
                )

            # if kwargs contain a __class__ del it
            if "__class__" in kwargs:
                del kwargs["__class__"]

            # set attributes from kwargs to self
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if hasattr(dictionary, "_sa_instance_state"):
            del dictionary["_sa_instance_state"]

        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage
        storage.delete(self)