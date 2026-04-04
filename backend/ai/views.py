import json
from .services import ChatService
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import StreamingHttpResponse


@method_decorator(csrf_exempt, name="dispatch")
class StreamChatView(View):
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
