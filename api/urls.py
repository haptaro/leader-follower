from django.urls import path
from .views import NoteEndpoint

urlpatterns = [
    # POST /api/notes/: Create a new note to the leader
    # GET  /api/notes/: Retrieve a list of notes from the leader
    path("", NoteEndpoint.as_view(), name="note-endpoint"),
]
