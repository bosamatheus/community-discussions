"""Comment router module."""

from typing import List, Union

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.api import deps
from app.domain.comment import Comment, UpdateComment
from app.usecase.comment import (
    CommentNotFoundToBeReplied,
    CommentUsecase,
    TopicNotFound,
)

router = APIRouter()


@router.get("", response_description="List comments by topic")
async def list_comments_by_topic(
    topic_id: str,
    skip: int = 0,
    limit: int = 10,
    usecase: CommentUsecase = Depends(deps.get_comment_usecase),
) -> List[Comment]:
    """List comments by topic."""
    comments = await usecase.find_by_topic(topic_id, skip, limit)
    return comments


@router.get(
    "/{comment_id}", response_description="Get a single comment in a topic"
)
async def get_comment(
    topic_id: str,
    comment_id: str,
    usecase: CommentUsecase = Depends(deps.get_comment_usecase),
) -> Union[Comment, JSONResponse]:
    """Get a single comment in a topic."""
    try:
        comment = await usecase.get(topic_id, comment_id)
    except TopicNotFound as err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=str(err)
        )
    else:
        if comment is not None:
            return comment
        raise HTTPException(
            status_code=404,
            detail=f"comment {comment_id} not found in topic {topic_id}",
        )


@router.post("", response_description="Create a new comment in a topic")
async def create_comment(
    topic_id: str,
    comment: Comment = Body(...),
    usecase: CommentUsecase = Depends(deps.get_comment_usecase),
) -> JSONResponse:
    """Create a new comment in a topic."""
    try:
        created_comment = await usecase.create(topic_id, comment)
    except (TopicNotFound, CommentNotFoundToBeReplied) as err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=str(err)
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=created_comment
        )


@router.put(
    "/{comment_id}",
    response_description="Update an existing comment in a topic",
)
async def update_comment(
    topic_id: str,
    comment_id: str,
    comment: UpdateComment = Body(...),
    usecase: CommentUsecase = Depends(deps.get_comment_usecase),
) -> Union[Comment, JSONResponse]:
    """Update an existing comment in a topic."""
    try:
        updated_comment = await usecase.update(topic_id, comment_id, comment)
    except TopicNotFound as err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=str(err)
        )
    else:
        if updated_comment is not None:
            return updated_comment
        raise HTTPException(
            status_code=404,
            detail=f"comment {comment_id} not found in topic {topic_id}",
        )


@router.delete(
    "/{comment_id}", response_description="Delete a comment in a topic"
)
async def delete_comment(
    topic_id: str,
    comment_id: str,
    usecase: CommentUsecase = Depends(deps.get_comment_usecase),
) -> JSONResponse:
    """Delete a comment in a topic."""
    try:
        deleted: bool = await usecase.delete(topic_id, comment_id)
    except TopicNotFound as err:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=str(err)
        )
    else:
        if deleted:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(
            status_code=404,
            detail=f"comment {comment_id} not found in topic {topic_id}",
        )
