from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func
from .database import Base  # Ensure Base is correctly defined in the database module
from sqlalchemy.orm import relationship

# Represents the Users table in the database
class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone_number = Column(String,unique=True, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    
# Represents the Posts table in the database
class Posts(Base):
    __tablename__ = "posts"
    
    post_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Users", backref="posts")
    
# Represents the Likes table in the database
class Likes(Base):
    __tablename__ = "likes"
    
    post_id = Column(Integer, ForeignKey("posts.post_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    
    post = relationship("Posts", backref="likes")
    user = relationship("Users", backref="likes")