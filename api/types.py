import strawberry
import strawberry_django
from django.contrib.auth.models import User
from api.models import Note, ChatRoom, Message


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


@strawberry_django.type(ChatRoom)
class ChatRoomType:
    id: strawberry.auto
    name: strawberry.auto
    created_at: strawberry.auto


@strawberry_django.type(Message)
class MessageType:
    id: strawberry.auto
    chat_room: ChatRoomType
    user: UserType
    content: strawberry.auto
    created_at: strawberry.auto
