from django.urls import path
from .views import NoteEndpoint
from .views import enqueue_30

urlpatterns = [
    # POST /api/notes/: Create a new note to the leader
    # GET  /api/notes/: Retrieve a list of notes from the leader
    path("notes/", NoteEndpoint.as_view(), name="note-endpoint"),
    path("enqueue-30/", enqueue_30, name="enqueue_30"),
]
