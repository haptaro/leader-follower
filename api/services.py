from api.models import Note, UserMetadata
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# Authentication Services
def signup_user(username: str, password: str) -> str:
    """
    Create a new user account and return an access token.
    
    Args:
        username: The desired username
        password: The user's password
        
    Returns:
        str: Access token for the new user
        
    Raises:
        Exception: If username already exists
    """
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        raise Exception("Username already exists")
    
    user = User.objects.create_user(username=username, password=password)
    # Create UserMetadata for the new user
    user_metadata, created = UserMetadata.objects.get_or_create(user=user)
    token = user_metadata.get_or_create_access_token()
    return token


def login_user(username: str, password: str) -> str:
    """
    Authenticate user and return access token.
    
    Args:
        username: The username
        password: The user's password
        
    Returns:
        str: Access token for the user
        
    Raises:
        Exception: If credentials are invalid
    """
    User = get_user_model()
    user = User.objects.filter(username=username).first()
    if not user or not user.check_password(password):
        raise Exception("Invalid credentials")
    
    # Ensure UserMetadata exists for the user
    user_metadata, created = UserMetadata.objects.get_or_create(user=user)
    return user_metadata.get_or_create_access_token()


def logout_user(user: User) -> str:
    """
    Log out user by clearing their access token.
    
    Args:
        user: The authenticated user
        
    Returns:
        str: Success message
        
    Raises:
        Exception: If user is not authenticated
    """
    if not user.is_authenticated:
        raise Exception("Authentication required")
    
    # Ensure UserMetadata exists for the user
    user_metadata, created = UserMetadata.objects.get_or_create(user=user)
    user_metadata.access_token = ''
    user_metadata.save()
    return "Logged out successfully"


# User Services
def get_authenticated_user(user: User) -> User | None:
    """
    Get the authenticated user if valid.
    
    Args:
        user: The user from request context
        
    Returns:
        User | None: The user if authenticated, None otherwise
    """
    if user.is_authenticated:
        return User.objects.get(pk=user.pk)
    return None


# Note Services
def find_my_notes(user_id: int) -> list[Note]:
    """
    Get all notes for a specific user, ordered by creation date (newest first).
    
    Args:
        user_id: The ID of the user
        
    Returns:
        list[Note]: List of notes for the user
    """
    return Note.objects.filter(user_id=user_id).order_by('-created_at')


def create_note(user: User, message: str) -> Note:
    """
    Create a new note for the authenticated user.
    
    Args:
        user: The authenticated user
        message: The note message
        
    Returns:
        Note: The created note
        
    Raises:
        Exception: If user is not authenticated
    """
    if not user.is_authenticated:
        raise Exception("Authentication required")
    
    note = Note.objects.create(message=message, user=user)
    return note
