import strawberry
import strawberry_django
from api.utils import IsAuthenticatedToken
from api.types import AddNoteInput, NoteType
from api import services


@strawberry.type
class Mutation:

    # Sign up
    @strawberry_django.mutation
    def signup(self, username: str, password: str) -> str:
        return services.signup_user(username, password)

    # Log in
    @strawberry_django.mutation
    def login(self, username: str, password: str) -> str:
        return services.login_user(username, password)

    # Log out
    @strawberry_django.mutation
    def logout(self, info) -> str:
        user = info.context.request.user
        return services.logout_user(user)

    # Add a new note
    @strawberry.mutation(permission_classes=[IsAuthenticatedToken])
    def add_note(self, info, input: AddNoteInput) -> NoteType:
        user = info.context.request.user
        return services.create_note(user, input.message)
    
