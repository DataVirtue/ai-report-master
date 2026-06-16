from rest_framework import serializers
from ai.models import Conversation, Message, SavedReport


class ChatMessageInputSerializer(serializers.Serializer):
    content = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["content", "role"]


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id", "title", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ConversationDetailSerializer(ConversationSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    report_id = serializers.SerializerMethodField()

    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ["messages", "report_id"]

    def get_report_id(self, obj):
        if obj.reports.first():
            return obj.reports.first().id
        return None


class SavedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = [
            "id",
            "title",
        ]
        read_only_fields = ["id"]
