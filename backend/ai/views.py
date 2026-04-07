import json
from .services import ChatService
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.renderers import BaseRenderer

class ServerSentEventRenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class StreamChatView(APIView):
    
    permission_classes = [AllowAny] 
    renderer_classes = [ServerSentEventRenderer]

    def dispatch(self, request, *args, **kwargs):
        self.service = ChatService(model="openai/o4-mini")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        messages = json.loads(request.GET.get("messages", "[]"))

        response = StreamingHttpResponse(
            self.stream(messages), content_type="text/event-stream"
        )

        response["Cache-Control"] = "no-cache"
        return response

    def stream(self, messages):
        yield from self.service.stream_messages(messages)
