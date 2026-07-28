from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Table, Integer, String, Float, ForeignKey


class Base(DeclarativeBase):
    pass

class Recipe(Base, Table):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    api_id: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    instructions: Mapped[str] = mapped_column(String)


class Ingredient(Base, Table):
    __tablename__ = "ingredients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float, default=None)
    price_url: Mapped[str] = mapped_column(String, default=None)


class recipe_ingredients(Base, Table):
    __tablename__ = "recipe_ingredients"
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity: Mapped[float] = mapped_column(Float, default=None)
    unit: Mapped[str] = mapped_column(String, default=None)