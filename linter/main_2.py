# uvicorn main_2:app --reload
# main - название файла с нашим приложением,
# app - название нашего приложения,
# --reload - будет автоматически перезапускаться при каждом обновлении кода

from typing import List, Sequence

from fastapi import FastAPI
from sqlalchemy import desc, update
from sqlalchemy.future import select

from linter.database import Base, engine, session
from linter.models_2 import RecipeInfo
from linter.schemas_2 import RecipeIn, RecipeOut, RecipesOut, SingleRecipeOut

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # здесь передаем синхронную функцию - create_all,
        # которую нужно дождаться
        await conn.run_sync(Base.metadata.create_all)

    # Наполнение данными
    # async with async_session() as session:
    #     async with session.begin():
    #         recipe_1 = RecipeInfo(title="Борщ",
    #                               cooking_time="120",
    #                               ingredients='Картошка, морковка,
    #                               лук, свекла, фасоль',
    #                               description='Все нарезать и сварить')
    #         recipe_2 = RecipeInfo(title="Яблочный пирог",
    #                               cooking_time="60",
    #                               ingredients='Яблоко, сахар,
    #                               мука, яйца, корица',
    #                               description='Смешать ингредиенты, запечь')
    #         recipe_3 = RecipeInfo(title="Клубничный коктейль",
    #                               cooking_time="5",
    #                               ingredients='Клубника, молоко, мороженое',
    #                               description='Взбить в блендере')
    #         recipe_4 = RecipeInfo(title="Салат Парус",
    #                               cooking_time="30",
    #                               ingredients='Корейская морковка, яйцо,
    #                               копченая курица, кукуруза,
    #                               чипсы, майонез',
    #                               description='Все нарезать
    #                               и выложить слоями')
    #
    #         session.add(recipe_1)
    #         session.add(recipe_2)
    #         session.add(recipe_3)
    #         session.add(recipe_4)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


# response model - объект pydentic - тип,
# к которому нужно сереализовать данные,
# которые возвращает эндпоинт
@app.get("/recipies", response_model=List[RecipesOut])
# List[RecipesOut] - это уже объект моделей sqlalchemy
async def recipies() -> Sequence[RecipeInfo]:
    # отправляем запрос в БД
    # Возвращает список рецептов по количеству просмотров
    res = await session.execute(select(RecipeInfo).order_by(desc(RecipeInfo.views)))
    return res.scalars().all()


# response model - объект pydentic - тип,
# к которому нужно сереализовать данные,
# которые возвращает эндпоинт
@app.get("/recipies/{recipe_id}", response_model=List[SingleRecipeOut])
# List[RecipeInfo] - это уже объект моделей sqlalchemy
async def recipies_by_id(recipe_id) -> Sequence[RecipeInfo]:
    # Получаем количество просмотров рецепта
    get_views = await session.execute(
        select(RecipeInfo.views).where(RecipeInfo.id == recipe_id)
    )
    views_res = int(get_views.scalars().all()[0])
    #  Увеличиваем количество просмотров на 1
    views_res += 1

    # Обновляем инфо в БД
    await session.execute(
        update(RecipeInfo).where(RecipeInfo.id == recipe_id).values(views=views_res)
    )
    await session.commit()

    # Оправляем обновленные данные пользователю
    res = await session.execute(select(RecipeInfo).where(RecipeInfo.id == recipe_id))
    return res.scalars().all()


# response model - тип,
# к которому нужно сереализовать данные,
# которые возвращает эндпоинт
@app.post("/write_recipe", response_model=RecipeOut)
async def write_recipe(recipe: RecipeIn) -> RecipeInfo:
    new_recipe = RecipeInfo(**recipe.dict())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe
