import strawberry
import strawberry_django
from api.utils import IsAuthenticatedToken
from api.types import UserType, NoteType, ChatRoomType, MessageType
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

    # Get all chat rooms
    @strawberry_django.field(permission_classes=[IsAuthenticatedToken])
    def chat_rooms(self, info) -> list[ChatRoomType]:
        return ChatRoom.objects.all()

    # Get messages in a specific chat room
    @strawberry_django.field(permission_classes=[IsAuthenticatedToken])
    def messages(self, info, chat_room_id: int) -> list[MessageType]:
        return Message.objects.filter(chat_room_id=chat_room_id).order_by('created_at')
