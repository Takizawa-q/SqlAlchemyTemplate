from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import DateTime, func

class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class TimestampMixin:
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())

class ReprMixin:
    
    def __repr__(self):
        
        columns = [c.name for c in self.__table__.columns]
        values = []
        for col in columns:
            value = getattr(self, col, None)
            if isinstance(value, str):
                values.append(f"{col}='{value}'")
            else:
                values.append(f"{col}={value}")
        class_name = self.__class__.__name__
        return f"{class_name}({', '.join(values)})"
