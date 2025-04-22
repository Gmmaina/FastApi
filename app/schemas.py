from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Base schema for user-related data
class UserBase(BaseModel):
    username: str  
    email: EmailStr
    phone_number: str
    password: str 
    
# Schema for user response (used when returning user data)
class UserResponse(BaseModel):
    user_id: int
    username: str  
    email: EmailStr
    phone_number: str
    
# Enables ORM mode for compatibility with ORMs like SQLAlchemy
    class Config:
        orm_mode = True  

# Schema for creating a new user
class CreateUser(UserBase):
    pass

# Schema for updating user details
class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None 
    
# Base schema for post-related data
class PostBase(BaseModel):
    title: str
    content: str

# Schema for post response (used when returning post data)
class PostResponse(PostBase):
    post_id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        orm_mode = True
        
class PostWithLikes(BaseModel):
    post: PostResponse
    likes: int  # Number of likes on the post
        
# Schema for creating a new post
class CreatePost(PostBase):
    pass  

# Schema for updating post details
class UpdatePost(BaseModel):
    title: Optional[str] = None  
    content: Optional[str] = None

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# Schema for authentication token
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data (used for extracting token-related information)
class TokenData(BaseModel):
    user_id: int

# Schema for likes on posts
class Like(BaseModel):
    post_id: int  # ID of the post being liked
    dir: int = Field(..., ge=0, le=1)  # Direction of the like (0 = unlike, 1 = like)