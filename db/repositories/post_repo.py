

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from db.models.post import Post

from .base_repo import BaseRepository


class PostRepository(BaseRepository[Post]):
    model_class = Post

    async def create_post(self, title: str, content: str, author_id: int) -> Post:
        """Create a new post"""
        post = Post(title=title, content=content, author_id=author_id)
        try:
            self.session.add(post)
            await self.session.flush()
            await self.session.refresh(post)
            await self.session.commit()  # Добавил commit для сохранения в БД
        except IntegrityError as e:
            await self.session.rollback()
            return None
        return post

    async def update_post(self, post: Post, title: str, content: str) -> Post | None:
        await self.session.execute(
            update(Post).where(Post.id == post.id).values(
                title=title, content=content)
        )
        # await self.session.commit()
        return post
