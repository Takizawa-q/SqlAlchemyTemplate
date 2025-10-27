from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, ReprMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import User


class Post(Base, TimestampMixin, ReprMixin):
    """Modern Post model with typed annotations and automatic timestamps."""
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(
        String(200), nullable=False)  # Убрал unique для title
    content: Mapped[str] = mapped_column(
        String(2000), nullable=False)  # Увеличил размер, убрал unique
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="posts")
