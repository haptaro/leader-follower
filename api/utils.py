from strawberry.permission import BasePermission
import typing
import strawberry
from django.contrib.auth.models import User
from api.models import UserMetadata

class IsAuthenticatedToken(BasePermission):
    message = "Not authenticated"

    def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs) -> bool:
        auth = info.context.request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return False
        
        token_str = auth.split("Bearer ")[1].strip()
        
        try:
            # Find user by access token
            user_metadata = UserMetadata.objects.select_related('user').get(access_token=token_str)
            user = user_metadata.user
            
            # Set the authenticated user in the request context for later use
            info.context.request.user = user
            info.context.request._cached_user = user
            
            return True
        except UserMetadata.DoesNotExist:
            return False
        except Exception:
            return False
