from pydantic import create_model, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from dao.dao import UserDAO
from dao.database import connection
from asyncio import run

from schemas import UserPydantic


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)


@connection
async def select_username_id(session):
    return await UserDAO.get_username_id(session)

@connection
async def select_full_user_info(session, user_id: int):
    rez = await UserDAO.get_user_info(session=session, user_id=user_id)
    if rez:
        return UserPydantic.model_validate(rez).model_dump()
    return {'message': f'Пользователь с ID {user_id} не найден!'}

@connection
async def select_full_user_info(session, user_id: int):
    rez = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    if rez:
        return UserPydantic.model_validate(rez).model_dump()
    return {'message': f'Пользователь с ID {user_id} не найден!'}

@connection(commit=False)
async def select_full_user_info_email(session: AsyncSession, user_id: int, email: str):
    FilterModel = create_model(
        'FilterModel',
        id=(int, ...),
        email=(EmailStr, ...)
    )

     #Также можно описать модель фильтра следующим образом
    # class FilterModel(BaseModel):
    #     id: int
    #     email: EmailStr

    user = await UserDAO.find_one_or_none(session=session, filters=FilterModel(id=user_id, email=email))

    if user:
        # Преобразуем ORM-модель в Pydantic-модель и затем в словарь
        return UserPydantic.model_validate(user).model_dump()

    return {'message': f'Пользователь с ID {user_id} не найден!'}

info = run(select_full_user_info_email(user_id=21, email='bob.smith@example.com'))
print(info)

