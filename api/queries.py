import strawberry
import strawberry_django
from api.utils import IsAuthenticatedToken
from api.types import UserType, NoteType
from api import services


@strawberry.type
class Query:

    # Get the currently authenticated user
    @strawberry.field(permission_classes=[IsAuthenticatedToken])
    def me(self, info) -> UserType | None:
        user = info.context.request.user
        return services.get_authenticated_user(user)
    
    # Get all notes for the authenticated user
    @strawberry_django.field(permission_classes=[IsAuthenticatedToken])
    def my_notes(self, info) -> list[NoteType]:
        user = info.context.request.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        
        return services.find_my_notes(user_id=user.pk)

