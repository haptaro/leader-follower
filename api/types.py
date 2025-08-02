import strawberry
import strawberry_django
from django.contrib.auth.models import User
from api.models import Note

@strawberry_django.type(User)
class UserType:
    id: strawberry.auto
    username: strawberry.auto
    email: strawberry.auto

@strawberry_django.type(Note)
class NoteType:
    id: strawberry.auto
    message: strawberry.auto
    created_at: strawberry.auto
    user: UserType

@strawberry_django.input(Note)
class AddNoteInput:
    message: strawberry.auto
