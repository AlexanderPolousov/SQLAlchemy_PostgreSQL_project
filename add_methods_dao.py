from dao.dao import UserDAO
from database import connection
from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession

from enum_models import GenderEnum, ProfessionEnum


@connection
async def add_one(user_data: dict, session: AsyncSession):
    new_user = await UserDAO.add(session=session, **user_data)
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user.id

@connection
async def add_many_users(users_data: list[dict], session=AsyncSession):
    new_users = await UserDAO.add_many(session=session, instances=users_data)
    user_ilds_list = [user.id for user in new_users]
    print(f"Добавлены новые пользователи с ID: {user_ilds_list}")
    return user_ilds_list

@connection
async def add_full_user(user_data: dict, session: AsyncSession):
    new_user = await UserDAO.add_user_with_profile(session=session, user_data=user_data)
    print(f"Добавлен новый пользователь с ID: {new_user.id}")
    return new_user.id



