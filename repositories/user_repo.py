
from models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def create_user(self, username: str, email: str, full_name: str) -> User:
        """Create a new user"""
        user = User(username=username, email=email, full_name=full_name)
        try:
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
        except IntegrityError:
            await self.session.rollback()
            return None
        return user
