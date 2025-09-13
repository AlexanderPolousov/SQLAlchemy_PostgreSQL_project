# DAO = Data Access Object - Объект Доступа к Данным
# DAO - это паттерн проектирования, который:
# Отделяет логику доступа к данным от бизнес-логики
# Инкапсулирует все операции с базой данных
# Предаставляет чистый API для работы с данными

from dao.base import BaseDAO
from models import User, Profile, Post, Comment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user_with_profile(cls, session: AsyncSession, user_data: dict)-> User:
        '''
        Добавляет пользователя и привязанный к нему профиль.
        Аргументы:
        - session: AsyncSession - асинхронная сессия базы данных
        - user_data: dict - словарь с данными пользователя и профиля
        Возвращает:
        - User - объект пользователя
        '''

        user = cls.model(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )
        session.add(user)
        await session.flush() # ПРОМЕЖУТОЧНЫЙ ШАГ для получения user.id без коммита
        #flush позволяет работать с данными, которые ещё не записаны в базу окончательно, но уже доступны для использования.
        ##########
        #Используя flush, мы избегаем нескольких коммитов. Это снижает нагрузку на базу данных, так как все изменения будут зафиксированы одним коммитом в конце транзакции.
        # Таким образом, база данных фиксирует изменения только один раз, что ускоряет выполнение операций.
        ##########
        #flush в SQLAlchemy отправляет изменения в базу данных без их окончательной фиксации,
        # то есть без выполнения коммита.
        # Это полезно, когда нужно сгенерировать данные, такие как идентификаторы (например, user.id),
        # чтобы ИСПОЛЬЗОВАТЬ ИХ ДО ФАКТИЧЕСКОГО СОХРАНЕНИЯ ДАННЫХ В БАЗЕ.
        # При этом сама транзакция остаётся открытой, и окончательное сохранение происходит позже, при вызове commit.

    #########################################################
        # Нюанс ВНИМАНИЕ здесь используем Profile
        # (создаем экземпляр именно от Profile)
        # выше мы создавали экземпляр user = cls.model так как находимся внутри class UserDAO(BaseDAO) и у нас есть
        #     model = User
        profile = Profile(
            user_id=user.id,
            first_name = user_data['first_name'],
            last_name = user_data.get('last_name'),
            age = user_data.get('age'),
            gender = user_data['gender'],
            profession = user_data.get('profession'),
            interests = user_data.get('interests'),
            contacts = user_data.get('contacts')
        )
        session.add(profile)
        await session.commit() # Один коммит для обоих действий

        return user

    ########## ПОЛУЧЕНИЕ - SELECT ДАННЫХ ##########

    @classmethod
    async def get_all_users(cls, session:AsyncSession): # Открытие сессии
        # создаем запрос к БД выбрать все данные из таблицы users
        query = select(cls.model)
        # сохраняем полученный результат в переменную result
        result = await session.execute(query) # execute(query) выполнять запрос ПОЛУЧИЛ ПОСЫЛКУ закрытую коробку от курьера
        records = result.scalars().all() # Извлекаем записи как объекты модели
        return records

    @classmethod
    async def get_username_id(cls, session: AsyncSession):
        # Создаем запрос для выборки id и username всех пользователей
        query = select(cls.model.id, cls.model.username)  # Указываем конкретные колонки
        print(query)  # Выводим запрос для отладки
        result = await session.execute(query)  # Выполняем асинхронный запрос
        records = result.all()  # Получаем все результаты
        return records  # Возвращаем список записей

    @classmethod
    async def get_user_info(cls, session: AsyncSession, user_id: int):
        query = select(cls.model).filter_by(id=user_id)
        # query = select(cls.model).filter(cls.model.id == user_id)
        result = await session.execute(query)
        user_info = result.scalar_one_or_none()
        return user_info



class ProfileDAO(BaseDAO):
    model = Profile

class PostDAO(BaseDAO):
    model = Post

class CommentDAO(BaseDAO):
    model = Comment





