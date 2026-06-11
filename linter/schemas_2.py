from pydantic import BaseModel

# данные классы используются для валидации и сериализации данных


# избегаем дублирования кода и выносим все общие детали в отдельный класс
class Recipes(BaseModel):
    title: str
    cooking_time: int


# Выдает все рецепты
class RecipesOut(Recipes):

    views: int

    # гооворим о том, что этот класс будет
    # использоваться для сериализации модели ORM
    class Config:
        orm_mode = True


# Выдает инфо по конкретному рецепту
class SingleRecipeOut(Recipes):

    views: int
    ingredients: str
    description: str

    # гооворим о том, что этот класс
    # будет использоваться для сериализации модели ORM
    class Config:
        orm_mode = True


class RecipeOut(Recipes):

    ingredients: str
    description: str
    views: int

    # гооворим о том, что этот класс
    # будет использоваться для сериализации модели ORM
    class Config:
        orm_mode = True


class RecipeIn(Recipes):
    ingredients: str
    description: str
