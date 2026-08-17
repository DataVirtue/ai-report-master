from email.mime import message
from requests import request
from rest_framework.serializers import Serializer
from rest_framework import serializers
from ai.models import Conversation, Report, SavedReport
from ai.serializers import (
    ConversationSerializer,
    ConversationDetailSerializer,
    ChatMessageInputSerializer,
    SavedReportSerializer,
    ReportNotificationSetupRequestSerializer,
)
from .services import ChatService, ReportGenerationService, ReportNotificationService
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from django.http import StreamingHttpResponse, response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
import logging
from django.shortcuts import get_object_or_404
import json
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

    def post(self, request, conversation_id=None):
        message = request.data.get("message")
        serializer = ChatMessageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data
        convo = Conversation.objects.filter(
            id=conversation_id, user=request.user
        ).first()
        if not convo:
            convo = Conversation.objects.create(user=request.user)

        response = StreamingHttpResponse(
            self.stream_from_conversation(convo.id, message),
            content_type="text/event-stream",
        )

        response["Cache-Control"] = "no-cache"
        return response

    def stream_from_conversation(self, conversation_id, message):
        conversation = get_object_or_404(Conversation, id=conversation_id)

        yield self.service._event("meta", data={"conversation_id": conversation_id})

        self.service.create_message(
            conversation, role="user", content=message["content"]
        )
        messages = list(
            conversation.messages.order_by("created_at").values("role", "content")
        )
        gen = self.stream(messages, conversation_id)
        final_message = None

        try:
            while True:
                event = next(gen)

                # 🔹 stream to client
                yield event

                # 🔹 parse event safely
                if event.startswith("data: "):
                    payload = json.loads(event[6:].strip())

                    if payload["type"] == "message":
                        final_message = payload["data"]

        except StopIteration:
            pass

        # 🔹 persist AFTER stream completes
        if final_message:
            self.service.create_message(conversation, "assistant", final_message)

        if conversation.title == "New Chat":
            messages = list(
                conversation.messages.order_by("created_at").values_list(
                    "content", flat=True
                )[:3]  # first few messages
            )

            title = self.service.get_conversation_title(messages)

            conversation.title = title
            conversation.save(update_fields=["title"])

            yield self.service._event("title", data=title)

    def stream(self, messages, conversation_id):
        yield from self.service.stream_messages(messages, conversation_id)


class ConversationViewsSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    serializer_action_classes = {
        "retrieve": ConversationDetailSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ChatService(model="openai/o4-mini")

    def get_serializer_class(self) -> type[Serializer]:
        return self.serializer_action_classes.get(self.action, ConversationSerializer)

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).order_by(
            "-updated_at", "-id"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def generate_title(self, request, pk=None):
        messages = request.data.get("messages", [])
        if not messages:
            return Response(
                {"error": "No messages found"}, status=status.HTTP_400_BAD_REQUEST
            )

        title = self.service.get_conversation_title(messages)

        return Response({"title": title})


class ReportView(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        self.report_service = ReportGenerationService()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, report_id, page_no):
        report = get_object_or_404(Report, id=report_id)
        sql = report.sql_query
        data = self.report_service.get_report(sql, page_no)
        return Response(data)


class SavedReportView(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        self.report_service = ReportGenerationService()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, report_id, page_no):
        report = get_object_or_404(SavedReport, id=report_id)
        sql = report.sql_query
        data = self.report_service.get_report(sql, page_no)
        return Response(data)


class SavedReportCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, report_id):
        title = request.data.get("title")
        report = get_object_or_404(Report, id=report_id)
        saved_report = SavedReport.objects.create(
            title=title if title else report.title,
            sql_query=report.sql_query,
            conversation=report.conversation,
            user=request.user,
        )

        return Response({"id": saved_report.id}, status=201)


class SavedReportViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedReportSerializer

    def get_queryset(self):
        return SavedReport.objects.filter(user=self.request.user).order_by("-id")


class EmailNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        self.notification_service = ReportNotificationService()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = ReportNotificationSetupRequestSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        report = SavedReport.objects.filter(id=validated_data.get("report_id")).first()

        self.notification_service.schedule_report(
            hour=validated_data.get("hr"),
            min=validated_data.get("min"),
            task_name=validated_data.get("task_name"),
            day=validated_data.get("day"),
            to_email_id=validated_data.get("to_email"),
            subject=validated_data.get("subject"),
            message=validated_data.get("message"),
            report_query=report.sql_query,
            filename=report.title,
            mimetype="text/csv",
        )
        return Response({"message": "Report Scheduled Successfullly"}, status=201)
