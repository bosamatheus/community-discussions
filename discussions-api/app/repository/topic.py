"""Topic repository module."""

from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.domain.topic import Topic
from app.repository.base import TopicRepository


class TopicRepositoryMongo(TopicRepository):
    """Topics repository MongoDB."""

    DISCUSSION_TYPE = "topic"

    def __init__(self, mongodb_client: AsyncIOMotorClient) -> None:
        self.mongodb = mongodb_client[TopicRepositoryMongo.COLLECTION_NAME]

    async def find(self, skip: int, limit: int) -> List[Topic]:
        """Find topics."""
        cursor = self.mongodb.find(
            {"type": TopicRepositoryMongo.DISCUSSION_TYPE}
        )
        cursor.skip(skip).limit(limit)
        topics: List[Topic] = []
        async for doc in cursor:
            topics.append(doc)
        return topics

    async def search(
        self,
        query: List[Dict[str, Any]],
        term: str = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Topic]:
        """Search for topics."""
        query.append({"type": TopicRepositoryMongo.DISCUSSION_TYPE})
        if term:
            query.append({"$text": {"$search": term}})
            cursor = self.mongodb.find(
                {"$and": query}, {"score": {"$meta": "textScore"}},
            )
            # Sorting results in ascending order by text score
            cursor.sort([("score", {"$meta": "textScore"})])
        else:
            cursor = self.mongodb.find({"$and": query})
        cursor.skip(skip).limit(limit)

        topics: List[Topic] = []
        async for doc in cursor:
            topics.append(doc)
        return topics

    async def get(self, topic_id: str) -> Optional[Topic]:
        """Get a topic."""
        topic = await self.mongodb.find_one(
            {"_id": topic_id, "type": TopicRepositoryMongo.DISCUSSION_TYPE}
        )
        return topic

    async def create(self, topic: Dict[str, Any]) -> str:
        """Create a topic."""
        result = await self.mongodb.insert_one(topic)
        return result.inserted_id

    async def update(self, topic_id: str, topic: Dict[str, Any]) -> int:
        """Update a topic."""
        result = await self.mongodb.update_one(
            {"_id": topic_id}, {"$set": topic}
        )
        return result.modified_count

    async def delete(self, topic_id: str) -> int:
        """Delete a topic."""
        result = await self.mongodb.delete_one({"_id": topic_id})
        return result.deleted_count
