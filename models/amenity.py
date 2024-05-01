#!/usr/bin/python3
"""Defines the Amenity class."""
from models.base_model import BaseModel

from models.base_model import Base
from models.place import Place
from sqlalchemy import Column, String, Table
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """This is the class for Amenity
    Attributes:
        name: input name
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    #  if we run into errors, look here
    place_amenities = relationship("Place", secondary="place_amenity")
