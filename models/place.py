#!/usr/bin/python3
"""Defines the Place class."""

from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
from models.user import User
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv


link_table = Table("place_amenity",
                   Base.metadata,
                   Column("place_id",
                          String(60),
                          ForeignKey("places.id")),
                   Column("amenity_id",
                          String(60),
                          ForeignKey("amenities.id")))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="all, delete")
    # took out back_populates, see if it is needed
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)

    if getenv("HBNB_TYPE_STORAGE", None) != "db":

        @property
        def reviews(self):
            """
            Returns the list of Review instances with place_id == current
            Place.id as private
            """
            c_list = []
            for key, value in models.storage.all(Review).items():
                if key.place_id == self.id:
                    return c_list.append(value)

        @property
        def amenities(self):
            """
            Returns list of Amenity instances based on attribute amenity_ids
            that contains all Amenity.id linked to the Place
            """
            a_list = []
            for key in models.storage.all(Amenity):
                if key.id in self.amenity_ids:
                    return a_list.append(key)

        @amenities.setter
        def amenities(self, value):
            """
            Handles append method for adding an Amenity.id to the attribute
            amenity_ids. This method should accept only Amenity object,
            otherwise, do nothing
            """
            if type(value) is Amenity:
                self.amenity_ids.append(value.id)
