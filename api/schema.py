import strawberry
import strawberry_django
from django.contrib.auth.models import User
from api.models import Note

from api.types import UserType, AddNoteInput, NoteType

@strawberry.type
class Query:
    @strawberry_django.field
    def me(self, info) -> UserType | None:
        user = info.context.request.user
        if user.is_authenticated:
            return User.objects.get(pk=user.pk)
        else:
            return None

@strawberry.type
class Mutation:
    @strawberry_django.mutation
    def add_note(self, info, input: AddNoteInput) -> NoteType:
        user = info.context.request.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        
        note = Note.objects.create(message=input.message, user=user)
        return note

schema = strawberry.Schema(query=Query, mutation=Mutation)
