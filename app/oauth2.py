from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from .database import get_db
from .config import settings

from app.schemas import TokenData

# OAuth2PasswordBearer is used to retrieve the token from the request
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# Load secret key, algorithm, and token expiration settings from the configuration
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Function to create a new access token
def create_access_token(data: dict):
    to_encode = data.copy()  # Copy the data to avoid modifying the original dictionary
    
    # Set the expiration time for the token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Add the expiration time to the token payload
    
    # Encode the token using the secret key and algorithm
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return jwt_token

# Function to verify the validity of an access token
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the user ID from the token payload
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception  # Raise an exception if user ID is missing
        
        # Create a TokenData object with the user ID
        token_data = TokenData(user_id=user_id)
    except JWTError:
        # Raise an exception if the token is invalid or decoding fails
        raise credentials_exception
    
    return token_data

# Function to retrieve the current user based on the access token
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    # Define the exception to be raised if credentials are invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    # Verify the access token and extract the token data
    token = verify_access_token(token, credentials_exception)
    
    # Query the database to retrieve the user based on the user ID in the token
    user = db.query(models.Users).filter(models.Users.user_id == token.user_id).first()
    
    return user