from typing import Optional, TypeVar, Generic, Type, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""
    model_class: Type[T] = None

    def __init__(self, session: AsyncSession):
        self.session = session
        if self.model_class is None:
            raise ValueError("model_class must be set in subclass")

    async def get(self, id: int) -> Optional[T]:
        """Get a single record by ID"""
        return await self.session.get(self.model_class, id)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        """Get all records with pagination"""
        stmt = select(self.model_class).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_all_with_relations(self, skip: int = 0, limit: int = 100, relations: list | object | None = None) -> list[T]:
        """Get all records with pagination and optional relations"""
        stmt = select(self.model_class)
        
        if relations:
            if isinstance(relations, object):
                stmt = stmt.options(selectinload(relations))
            else:
                for relation in relations:
                    stmt = stmt.options(selectinload(relation))
        
        stmt = stmt.offset(skip).limit(limit)
        print(stmt)
        result = await self.session.execute(stmt)
        print("DONE")
        return list(result.scalars().all())
    
    async def create(self, **kwargs) -> T:
        """Create a new record"""
        obj = self.model_class(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj
    
    async def update(self, id: int, **kwargs) -> Optional[T]:
        """Update a record"""
        obj = await self.get(id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await self.session.flush()
            await self.session.refresh(obj)
        return obj
    
    async def delete(self, id: int) -> bool:
        """Delete a record"""
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)
            await self.session.flush()
            return True
        return False
    
    async def commit(self):
        """Commit the transaction"""
        await self.session.commit()
    
    async def rollback(self):
        """Rollback the transaction"""
        await self.session.rollback()