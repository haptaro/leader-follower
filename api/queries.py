import strawberry
import strawberry_django
from django.contrib.auth.models import User
from api.utils import IsAuthenticatedToken

from api.types import UserType, NoteType
from api.services import find_my_notes

@strawberry.type
class Query:

    # Get the currently authenticated user
    @strawberry.field(permission_classes=[IsAuthenticatedToken])
    def me(self, info) -> UserType | None:
        user = info.context.request.user
        if user.is_authenticated:
            return User.objects.get(pk=user.pk)
        else:
            return None
    
    # Get all notes for the authenticated user
    @strawberry_django.field(permission_classes=[IsAuthenticatedToken])
    def my_notes(self, info) -> list[NoteType]:
        user = info.context.request.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        
        return find_my_notes(user_id=user.pk)

