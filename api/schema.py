import strawberry
import strawberry_django
from django.contrib.auth.models import User

from api.types import UserType

@strawberry.type
class Query:
    @strawberry_django.field
    def me(self, info) -> UserType | None:
        user = info.context.request.user
        if user.is_authenticated:
            return User.objects.get(pk=user.pk)
        else:
            return None


schema = strawberry.Schema(query=Query)
