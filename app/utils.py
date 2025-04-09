from passlib.context import CryptContext    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt.
    
    Args:
        password (str): The password to be hashed.
        
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies the password against the hashed password.
    
    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.
        
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)