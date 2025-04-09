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
    COMMENT:
    - This function uses SQLAlchemy to query the database for a user matching the provided username or email.
    - Password verification is performed using a utility function.
    - If authentication is successful, an access token is generated using the OAuth2 mechanism.
    """
    user = db.query(models.Users).filter(
        or_(
            models.Users.email == user_credentials.username,
            models.Users.username == user_credentials.username
        )
        ).first()
   
    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
            )
   

    access_token = oauth2.create_access_token(data={"user_id": user.user_id})
    
    return {
        "Login_success": True,
        "access_token": access_token,
        "token_type": "bearer"
    }