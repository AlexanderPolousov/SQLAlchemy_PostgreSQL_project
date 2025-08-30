from typing import List
from sqlalchemy import ForeignKey, text, ARRAY, String, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, uniq_str_an
from enum_models import GenderEnum, ProfessionEnum, StatusPost, RatingEnum

class User(Base):
    username: Mapped[uniq_str_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("profiles.id"))

class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    interests: Mapped[List[str] | None] = mapped_column(ARRAY(String))
    contacts: Mapped[dict | None] = mapped_column(JSON)

class Post(Base):
    title: Mapped[str]
    content: Mapped[Text]
    main_photo_url: Mapped[str]
    photos_url: Mapped[List[str] | None] = mapped_column(ARRAY(String))
    status: Mapped[StatusPost] = mapped_column(default=StatusPost.PUBLISHED, server_default=text("'DRAFT'"))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

class Comment(Base):
    content: Mapped[Text]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published: Mapped[bool] = mapped_column(default=True, server_default=text("'false'"))
    rating: Mapped[RatingEnum] = mapped_column(default=RatingEnum.FIVE, server_default=text("'SEVEN'"))