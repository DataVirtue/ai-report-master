from ai.models import Conversation
from ai.serializers import ConversationSerializer
from .services import ChatService
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
import logging

logger = logging.getLogger(__name__)


class ServerSentEventRenderer(BaseRenderer):
    media_type = "text/event-stream"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            error_msg = data.get("detail", str(data))
            error_payload = {
                "type": "data",
                "data": {"error": str(error_msg), "rows": []},
            }
            import json

            return f"data: {json.dumps(error_payload)}\n\n"
        return data


class StreamChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [ServerSentEventRenderer]

    def dispatch(self, request, *args, **kwargs):
        self.service = ChatService(model="openai/o4-mini")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        messages = request.data.get("messages", [])
        if isinstance(messages, str):
            import json

            messages = json.loads(messages)

        response = StreamingHttpResponse(
            self.stream(messages), content_type="text/event-stream"
        )

        response["Cache-Control"] = "no-cache"
        return response

    def stream(self, messages):
        yield from self.service.stream_messages(messages)


class ConversationViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
