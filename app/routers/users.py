from fastapi import APIRouter, Depends, HTTPException, Response, status   
from sqlalchemy.orm import Session
from typing import List
from .. import models
from ..database import get_db
from ..schemas import UserResponse, UpdateUser, CreateUser
from ..utils import hash_password

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

# Route to get all users
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()    
    return users

# Route to create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    # Hash the password before saving
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    
    try:
        new_user = models.Users(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="failed to create user")    

# Route to get a specific user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

# Route to delete a user by ID
@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    User = db.query(models.Users).filter(models.Users.user_id == user_id)
    if User.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    User.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Route to update a user's details by ID
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    existing_user = db.query(models.Users).filter(models.Users.user_id == user_id)
    update_user = existing_user.first()
    
    if update_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    existing_user.update(user.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(update_user) 
    
    return update_user
