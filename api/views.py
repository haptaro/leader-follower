from rest_framework.generics import ListCreateAPIView
from .models import Note
from .serializers import NoteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import dummy_task
from strawberry.django.views import GraphQLView

@api_view(["POST"])
def enqueue_30(request):
    return Response({"queued": 30})


class NoteEndpoint(ListCreateAPIView):
    queryset           = Note.objects.all().order_by("-id")
    serializer_class   = NoteSerializer


class APIGraphQLView(GraphQLView):
    def get_context(self, request, response=None):
        return {"request": request, "response": response}
