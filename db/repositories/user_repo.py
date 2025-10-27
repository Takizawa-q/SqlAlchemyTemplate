

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from db.models.user import User

from .base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    model_class = User

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def get_posts(self, user: User) -> list:
        """Get all posts for a specific user"""
        from db.models.post import Post
        result = await self.session.execute(
            select(Post).where(Post.author_id == user.id)
        )
        return list(result.scalars().all())

    async def create_user(self, username: str, email: str, full_name: str) -> User:
        """Create a new user"""
        user = User(username=username, email=email, full_name=full_name)
        try:
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
        except IntegrityError as e:
            await self.session.rollback()
            return None
        return user

    async def update_user_email(self, user: User, new_email: str) -> User | None:
        await self.session.execute(
            update(User).where(User.id == user.id).values(email=new_email)
        )
        # await self.session.commit()
        return user
