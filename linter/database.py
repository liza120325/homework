from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base

# 1. Строка подключения
DATABASE_URL = "sqlite+aiosqlite:///./recipes.db"

# 2. Создание асинхронного движка
# echo=True будет логгировать в консоль все sql запросу,
# которые мы будем делать
engine = create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.

# 3. Фабрика асинхронных сессий
async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
session = async_session()
Base = declarative_base()
