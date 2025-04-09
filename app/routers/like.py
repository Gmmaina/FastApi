from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, database, oauth2
 

router = APIRouter(
    prefix="/likes",
    tags=["likes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # Check if the post exists
    post = db.query(models.Posts).filter(models.Posts.post_id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Check if the user has already liked the post
    like_query = db.query(models.Likes).filter(
        models.Likes.post_id == like.post_id,
        models.Likes.user_id == current_user.user_id
    )
    
    existing_like = like_query.first()
    
    # If the user is liking the post
    if(like.dir == 1):
        if existing_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already liked this post")
        new_like = models.Likes(post_id=like.post_id, user_id=current_user.user_id)
        db.add(new_like)
        db.commit()
        return {"message": "Post liked successfully"}
    else:
        if not existing_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not liked this post")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Post unliked successfully"}