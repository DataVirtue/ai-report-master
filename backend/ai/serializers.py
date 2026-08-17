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


class ReportNotificationSetupRequestSerializer(serializers.Serializer):
    to_email = serializers.EmailField()
    report_id = serializers.IntegerField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField(max_length=1000)
    hr = serializers.IntegerField()
    min = serializers.IntegerField()
    day = serializers.IntegerField()
    task_name = serializers.CharField(max_length=100)

    def validate_hr(self, value):
        if value > 23 or value < 0:
            raise serializers.ValidationError("Invalid Hours Value")
        return value

    def validate_min(self, value):
        if value > 59 or value < 0:
            raise serializers.ValidationError("Invalid Min Value")
        return value

    def validate_day(self, value):
        if value > 6 or value < 0:
            raise serializers.ValidationError("Invalid Day Value")
        return value

    def validate_report_id(self, value):
        if not SavedReport.objects.filter(id=value).exists():
            raise serializers.ValidationError("Report Id does not exists")
        return value
