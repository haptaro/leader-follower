from rest_framework.generics import ListCreateAPIView
from .models import Note
from .serializers import NoteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import dummy_task
from strawberry.django.views import GraphQLView

@api_view(["POST"])
def enqueue_30(request):
    for i in range(30):
        dummy_task.delay(i)
    return Response({"queued": 30})


class NoteEndpoint(ListCreateAPIView):
    queryset           = Note.objects.all().order_by("-id")
    serializer_class   = NoteSerializer


class APIGraphQLView(GraphQLView):
    pass
