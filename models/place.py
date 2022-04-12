#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models import storage
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table('place_amenity', Base.metadata,
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

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        amenity_ids = []
        reviews = relationship(
            "Review",
            backref="Place",
            cascade="all, delete-orphan"
        )
        amenities = relationship(
            "Amenity",
            # backref="Place",
            # cascade="all, delete-orphan",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities"
        )

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def get_reviews(self):
            listReview = []
            for k in storage.__object:
                if (k["__class__"] == "Review") and k["place_id"] == self.id:
                    listReview.append(k)
            return listReview

        @property
        def amenities(self):
            """ get list amenty.ids """
            return self.amenity_ids

        @amenities.setter
        def amenities(self):
            """ set amenities """
            self.amenity_ids = []
            for k in storage.__object:
                if (k["__class__"] == "Amenity") and k["amenity_id"] == self.id:
                    self.amenity_ids.append(k.id)
