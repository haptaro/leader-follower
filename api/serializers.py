from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Note
        fields = ["id", "message", "created_at"]
