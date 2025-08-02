import strawberry
import strawberry_django
from api.models import Note, UserMetadata
from django.contrib.auth import get_user_model
from api.utils import IsAuthenticatedToken

from api.types import AddNoteInput, NoteType

@strawberry.type
class Mutation:

    # Sign up
    @strawberry_django.mutation
    def signup(self, username: str, password: str) -> str:
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise Exception("Username already exists")
        user = User.objects.create_user(username=username, password=password)
        # Create UserMetadata for the new user
        user_metadata, created = UserMetadata.objects.get_or_create(user=user)
        token = user_metadata.get_or_create_access_token()
        return token

    # Log in
    @strawberry_django.mutation
    def login(self, username: str, password: str) -> str:
        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            raise Exception("Invalid credentials")
        # Ensure UserMetadata exists for the user
        user_metadata, created = UserMetadata.objects.get_or_create(user=user)
        return user_metadata.get_or_create_access_token()

    # Log out
    @strawberry_django.mutation
    def logout(self, info) -> str:
        user = info.context.request.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        # Ensure UserMetadata exists for the user
        user_metadata, created = UserMetadata.objects.get_or_create(user=user)
        user_metadata.access_token = ''
        user_metadata.save()
        return "Logged out successfully"

    # Add a new note
    @strawberry.mutation(permission_classes=[IsAuthenticatedToken])
    def add_note(self, info, input: AddNoteInput) -> NoteType:
        user = info.context.request.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        
        note = Note.objects.create(message=input.message, user=user)
        return note
    
