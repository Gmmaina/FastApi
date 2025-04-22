from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional

from app import oauth2
from .. import models
from ..database import get_db
from ..schemas import PostResponse, PostWithLikes, UpdatePost, CreatePost, UserResponse

# Create a router for handling post-related endpoints
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Endpoint to create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # Print the email of the current user (for debugging purposes)
    print(current_user.email)
    try:
        # Create a new post with the current user's ID as the owner
        new_post = models.Posts(owner_id=current_user.user_id, **post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        return new_post
    except Exception:
        # Raise an HTTP exception if the post creation fails
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="failed to create post")

# Endpoint to update an existing post
@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: UpdatePost, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # Query the database for the post with the given ID
    existing_post = db.query(models.Posts).filter(models.Posts.post_id == post_id)
    update_post = existing_post.first()
    
    # Check if the post exists
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Check if the current user is the owner of the post
    if update_post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    
    # Update the post with the provided data
    existing_post.update(post.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(update_post)
    
    return update_post

# Endpoint to retrieve a list of posts with optional search, limit, and skip parameters
@router.get("/", response_model=List[PostWithLikes])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # Query the database for posts that match the search term
    # posts = db.query(models.Posts).filter(models.Posts.content.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Posts, func.count(models.Likes.post_id).label("likes_count")).join(models.Likes, models.Posts.post_id == models.Likes.post_id, isouter=True).group_by(models.Posts.post_id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    
    # Serialize the query result into the expected response format
    return [
        {
            "post": {
                "post_id": post.post_id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "owner_id": post.owner_id,
                "owner": {
                    "user_id": post.owner.user_id,
                    "username": post.owner.username,
                    "email": post.owner.email,
                    "phone_number": post.owner.phone_number
                }
            },
            "likes": likes
        }
        for post, likes in posts
    ]

# Endpoint to retrieve a single post by its ID
@router.get("/{post_id}", response_model=PostWithLikes)
def get_post(post_id: int, db: Session = Depends(get_db)):
    
    # Query the database for the post with the given ID
    # post = db.query(models.Posts).filter(models.Posts.post_id == post_id).first()
    
    post_query = db.query(models.Posts, func.count(models.Likes.post_id).label("likes_count")).join(models.Likes, models.Posts.post_id == models.Likes.post_id, isouter=True).group_by(models.Posts.post_id).filter(models.Posts.post_id == post_id).first()
    
    # Check if the post exists
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post, likes_count = post_query
    
    # Serialize the query result into the expected response format    
    response = PostWithLikes(
        post = PostResponse(
            post_id = post.post_id,
            title = post.title,
            content = post.content,
            created_at = post.created_at,
            owner_id = post.owner_id,
            owner = UserResponse(
                username = post.owner.username,
                email = post.owner.email
                
            )
        ),
        likes = likes_count
    )
    
    return response

# Endpoint to delete a post by its ID
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # Query the database for the post with the given ID
    post_query = db.query(models.Posts).filter(models.Posts.post_id == post_id)
    post = post_query.first()
    
    # Check if the post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Check if the current user is the owner of the post
    if post.owner_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    
    # Delete the post from the database
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)