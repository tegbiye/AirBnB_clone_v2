#!/usr/bin/python3
"""Defines the Review class."""

from models.base_model import BaseModel
from models.base_model import Base

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Review(BaseModel, Base):
    """This is the class for Review
    Attributes:
        place_id: place id
        user_id: user id
        text: review description
    """

    """This init method allows the class to access BaseModel's attributes"""

    __tablename__ = "reviews"

    place_id = Column(String(60),ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60),ForeignKey("users.id"), nullable=False)
    text = Column(String(1024), nullable=False)
