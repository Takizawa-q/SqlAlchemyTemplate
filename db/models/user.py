from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, ReprMixin, TimestampMixin

if TYPE_CHECKING:
    from .post import Post


class User(Base, TimestampMixin, ReprMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
        # Автоматическое удаление постов при удалении пользователя
        cascade="all, delete-orphan"
    )
