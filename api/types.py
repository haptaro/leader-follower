import strawberry
import strawberry_django
from django.contrib.auth.models import User

@strawberry_django.type(User)
class UserType:
    id: strawberry.auto
    username: strawberry.auto
    email: strawberry.auto
