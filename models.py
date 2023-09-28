# This file contains the SQLAlchemy models
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # This attribute will contain a Item SQLAlchemy model
    # from the items table. The cascade option will make sure
    # that all items from a user are deleted if that user is deleted from the db.
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # This attribute will contain a User SQLAlchemy model
    # from the users talbe.
    owner = relationship("User", back_populates="items")