import json
from ai.services import chat_service
from django.shortcuts import render
from rest_framework.response import Response
from .services import ChatService, ReportGenerationService
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView


# Create your views here.
#
#
#
@method_decorator(csrf_exempt, name="dispatch")
class ChatView(APIView):
    chat_service = ChatService(model="openai/o4-mini")

    def post(self, request):
        messages = request.data.get("messages")
        response = self.chat_service.send_messages(messages)

        return Response(
            {
                "message": response,
            }
        )
