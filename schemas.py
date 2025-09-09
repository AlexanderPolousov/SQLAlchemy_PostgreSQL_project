from pydantic import BaseModel, ConfigDict
from enum_models import GenderEnum, ProfessionEnum


class ProfilePydantic(BaseModel):
    first_name: str
    last_name: str | None
    age: int | None
    gender: GenderEnum
    profession: ProfessionEnum
    interests: list[str] | None
    contacts: dict | None
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    #from_attributes = True: это позволяет модели автоматически маппить атрибуты Python объектов на поля модели.
    # Примерно то что мы делали в методе to_dict, но более расширенно
    #use_enum_values = True: это указание преобразовывать значения перечислений в их фактические значения,
    # а не в объекты перечислений. Просто для удобства восприятия человеком.

class UserPydantic(BaseModel):
    username: str
    email: str
    profile: ProfilePydantic | None
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class UsernameIdPydantic(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
