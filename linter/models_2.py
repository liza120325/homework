from sqlalchemy import Column, Integer, String

from linter.database import Base

# модели таблиц sqlalchemy


# модель информации о рецепте
class RecipeInfo(Base):
    __tablename__ = "recipie_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True)
    cooking_time = Column(Integer, index=True)
    ingredients = Column(String, index=True)
    description = Column(String, index=True)
    views = Column(Integer, default=0)
