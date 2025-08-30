from datetime import datetime
from sqlalchemy import Integer, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import  AsyncAttrs, async_sessionmaker, create_async_engine
from config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls)-> str:
        return cls.__name__.lower() + "s"


# DeclarativeBase: Основной класс для всех моделей, от которого будут наследоваться все таблицы (модели таблиц). Эту особенность класса мы будем использовать неоднократно.
# AsyncAttrs: Позволяет создавать асинхронные модели, что улучшает производительность при работе с асинхронными операциями.
# create_async_engine: Функция, создающая асинхронный движок для соединения с базой данных по предоставленному URL.
# async_sessionmaker: Фабрика сессий для асинхронного взаимодействия с базой данных. Сессии используются для выполнения запросов и транзакций.
# Как это работает
# DATABASE_URL: Формируется с помощью метода get_db_url из файла конфигурации config.py. Содержит всю необходимую информацию для подключения к базе данных.
# engine: Асинхронный движок, необходимый для выполнения операций с базой данных.
# async_session_maker: Фабрика сессий, которая позволяет создавать сессии для взаимодействия с базой данных, управлять транзакциями и выполнять запросы.
# Base: Абстрактный базовый класс для всех моделей, от которого будут наследоваться все таблицы. Он не создаст отдельную таблицу в базе данных, но предоставит базовую функциональность для всех других моделей.

# В базовом классе Base определены три колонки (id, created_at, updated_at), которые будут добавляться ко всем моделям, унаследованным от Base:
# id: Первичный ключ, который автоматически инкрементируется.
# created_at: Дата и время создания записи, задаются автоматически.
# updated_at: Дата и время последнего обновления записи, автоматически обновляется при каждом изменении.

# ПРИМЕР класса User
# class User(Base):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

# id: Целочисленный первичный ключ, который автоматически инкрементируется.
# name: Строка, которая не может быть пустой (nullable=False).
# email: Уникальная строка, которая также не может быть пустой.

#surname: Mapped[str | None]: Поле surname необязательно (nullable=True), так как тип данных указывает на то,
# что оно может быть None. Нет необходимости явно указывать mapped_column(String, nullable=True).


