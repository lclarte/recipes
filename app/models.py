from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    recipes = relationship("Recipe", back_populates="author")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="recipes")
    images = relationship("RecipeImage", back_populates="recipe", cascade="all, delete-orphan")


class RecipeImage(Base):
    __tablename__ = "recipe_images"

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    filename = Column(String(255), nullable=False)

    recipe = relationship("Recipe", back_populates="images")
