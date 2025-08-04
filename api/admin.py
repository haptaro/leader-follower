from django.contrib import admin
from .models import Note, UserMetadata, ChatRoom, ChatRoomMember, Message

admin.site.register(Note)
admin.site.register(UserMetadata)
admin.site.register(ChatRoom)
admin.site.register(ChatRoomMember)
admin.site.register(Message)
