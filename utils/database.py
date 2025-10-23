from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, AsyncGenerator, Generic, Optional, TypeVar

from sqlalchemy import DateTime, Integer, func, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import config
from utils.dsn_generator import SQLAlchemyDSNGenerator


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())


class DatabaseManager(SQLAlchemyDSNGenerator):
    """Modern async SQLAlchemy database manager with comprehensive CRUD operations."""

    def __init__(self):
        print("I AM IN DATABASE MANAGER")
        dsn = self.postgresql(
            username=config.db.user,
            password=config.db.password,
            host=config.db.host,
            port=config.db.port,
            database=config.db.database
        )

        self.engine = create_async_engine(
            dsn,
            echo=config.app.debug,  # Enable SQL logging in debug mode
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,  # Validate connections before use
        )

        self.async_session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def session(self, auto_commit: bool = False) -> AsyncGenerator[AsyncSession, None]:
        """
        Context manager for database sessions with optional auto-commit.

        Args:
            auto_commit: If True, automatically commit on success
        """
        async with self.async_session_maker() as session:
            try:
                yield session
                if auto_commit:
                    await session.commit()
            except Exception as e:
                await session.rollback()
                raise

    # Database lifecycle methods
    async def init_db(self, base: Optional[DeclarativeBase] = None):
        """Create all database tables"""
        base = base or Base  # ✅ Use passed base or default to Base
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

    async def drop_db(self, base: Optional[DeclarativeBase] = None):
        """Drop all database tables"""
        base = base or Base  # ✅ Fix this one too
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.drop_all)

    async def close(self):
        """Close the database engine and all connections."""
        await self.engine.dispose()

    async def execute_raw_sql(self, session: AsyncSession, sql: str, params: Optional[dict] = None) -> Any:
        """Execute raw SQL query with optional parameters."""
        try:
            result = await session.execute(text(sql), params or {})
            return result
        except SQLAlchemyError as e:
            raise

db = DatabaseManager()
