import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Association table for the many-to-many relationship between User and Favorite
user_favorite = Table(
    'user_favorite', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('favorite_id', Integer, ForeignKey('favorites.id'), primary_key=True)
)

# Association table for the many-to-many relationship between User and Planet
user_planet = Table(
    'user_planet', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planets.id'), primary_key=True)
)

# Association table for the many-to-many relationship between User and Character
user_character = Table(
    'user_character', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True)
)

# Association table for the many-to-many relationship between User and Spaceship
user_spaceship = Table(
    'user_spaceship', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('spaceship_id', Integer, ForeignKey('spaceships.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    subscription_date = Column(DateTime, nullable=False)

    # Relationships
    favorites = relationship("Favorite", secondary=user_favorite, back_populates="users")
    favorite_planets = relationship("Planet", secondary=user_planet, back_populates="users")
    favorite_characters = relationship("Character", secondary=user_character, back_populates="users")
    favorite_spaceships = relationship("Spaceship", secondary=user_spaceship, back_populates="users")

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)  # "planet", "character", or "spaceship"
    name = Column(String(200), nullable=False)

    # Relationships
    users = relationship("User", secondary=user_favorite, back_populates="favorites")

class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    climate = Column(String(100), nullable=False)
    terrain = Column(String(100), nullable=False)
    population = Column(Integer)

    # Relationships
    users = relationship("User", secondary=user_planet, back_populates="favorite_planets")

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    gender = Column(String(50))
    birth_year = Column(String(50))
    height = Column(String(50))

    # Relationships
    users = relationship("User", secondary=user_character, back_populates="favorite_characters")

class Spaceship(Base):
    __tablename__ = 'spaceships'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    model = Column(String(100), nullable=False)
    manufacturer = Column(String(100))
    capacity = Column(Integer)

    # Relationships
    users = relationship("User", secondary=user_spaceship, back_populates="favorite_spaceships")

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
