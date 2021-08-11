"""Usecase module."""

from typing import List, Optional

from fastapi.encoders import jsonable_encoder

from discussion.repository.topic import TopicRepositoryMongo
from discussion.repository.comment import CommentRepositoryMongo
from discussion.domain.comment import Comment, UpdateComment


class CommentUsecase:
    """Comments usecase."""

    def __init__(
        self, topic_repo: TopicRepositoryMongo, comment_repo: CommentRepositoryMongo
    ) -> None:
        self.topic_repo = topic_repo
        self.comment_repo = comment_repo

    async def find_by_topic(
        self, topic_id: str, skip: int, limit: int
    ) -> List[Comment]:
        """Find comments by topic."""
        comments: List[Comment] = await self.comment_repo.find_by_topic(
            topic_id, skip, limit
        )
        return comments

    async def get(self, topic_id: str, comment_id: str) -> Optional[Comment]:
        """Get a single comment in a topic."""
        topic_exists = await self.__check_topic_exists(topic_id)
        if not topic_exists:
            raise RuntimeError(f"topic {topic_id} does not exist")

        comment = await self.comment_repo.get(topic_id, comment_id)
        return comment

    async def create(self, topic_id: str, comment: Comment) -> Optional[Comment]:
        """Create a comment in a topic."""
        topic_exists = await self.__check_topic_exists(topic_id)
        if not topic_exists:
            raise RuntimeError(f"topic {topic_id} does not exist")

        reply_comment_id = comment.reply_comment
        if reply_comment_id:
            reply_comment = await self.comment_repo.get(topic_id, reply_comment_id)
            if not reply_comment:
                raise RuntimeError(
                    f"comment {reply_comment_id} does not exist to reply"
                )

        comment.topic_id = topic_id
        inserted_id = await self.comment_repo.create(jsonable_encoder(comment))
        created_comment = await self.comment_repo.get(topic_id, inserted_id)
        return created_comment

    async def update(
        self, topic_id: str, comment_id: str, comment: UpdateComment
    ) -> Optional[Comment]:
        """Update a comment in a topic."""
        topic_exists = await self.__check_topic_exists(topic_id)
        if not topic_exists:
            raise RuntimeError(f"topic {topic_id} does not exist")

        # Cleaning up the request body
        comment_clean = {k: v for k, v in comment.dict().items() if v is not None}
        if len(comment_clean) >= 1:
            modified_count = await self.comment_repo.update(
                topic_id, comment_id, comment_clean
            )
            if modified_count == 1:
                if (
                    updated_comment := await self.comment_repo.get(topic_id, comment_id)
                ) is not None:
                    return updated_comment

        if (
            existing_comment := await self.comment_repo.get(topic_id, comment_id)
        ) is not None:
            return existing_comment

    async def delete(self, topic_id: str, comment_id: str) -> bool:
        """Delete a comment in a topic."""
        topic_exists = await self.__check_topic_exists(topic_id)
        if not topic_exists:
            raise RuntimeError(f"topic {topic_id} does not exist")

        deleted_count: int = await self.comment_repo.delete(topic_id, comment_id)
        return deleted_count > 0

    async def __check_topic_exists(self, topic_id: str) -> bool:
        """Check if a topic exists."""
        topic = await self.topic_repo.get(topic_id)
        return topic is not None
