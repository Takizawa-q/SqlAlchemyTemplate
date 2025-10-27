# Импортируем модели в правильном порядке
from .post import Post  # Потом Post (зависимая модель)
from .user import User  # Сначала User (родительская модель)

# Экспортируем все модели
__all__ = ["User", "Post"]
