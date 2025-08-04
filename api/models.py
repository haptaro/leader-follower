from django.db import models

class Note(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'auth.User',
        related_name='notes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.message[:30]


class UserMetadata(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, blank=True, db_index=True)

    def __str__(self):
        return f"{self.user.username}'s metadata"

    def generate_token(self):
        import secrets
        return secrets.token_urlsafe(32)

    def get_or_create_access_token(self):
        if not self.access_token:
            self.access_token = self.generate_token()
            self.save()
        return self.access_token


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatRoomMember(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='chat_rooms')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('chat_room', 'user')


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
