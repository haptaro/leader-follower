from rest_framework.generics import ListCreateAPIView
from .models import Note
from .serializers import NoteSerializer

class NoteEndpoint(ListCreateAPIView):
    queryset           = Note.objects.all().order_by("-id")
    serializer_class   = NoteSerializer
