from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.schemas import Token
from .. import models, oauth2, utils

router = APIRouter(
    tags=["Authentication"]
)
@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Handle user login by verifying credentials and generating an access token.
    Args:
        user_credentials (OAuth2PasswordRequestForm): The user credentials provided in the login request.
        db (Session): The database session dependency.
    Returns:
        dict: A dictionary containing the login status, access token, and token type.
    Raises:
        HTTPException: If the user credentials are invalid or the user does not exist.
    """
    # Validate input fields
    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username and password are required"
        )

    # Query the database for the user
    user = db.query(models.Users).filter(
        or_(
            models.Users.email == user_credentials.username,
            models.Users.username == user_credentials.username
        )
    ).first()
   
    # Verify user and password
    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
   
    # Generate access token
    access_token = oauth2.create_access_token(data={"user_id": user.user_id})
    
    return {
        "Login_success": True,
        "access_token": access_token,
        "token_type": "bearer"
    }