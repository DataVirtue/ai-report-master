from rest_framework import serializers

from ai.models import Conversation, Message

class ChatMessageInputSerializer(serializers.Serializer):
    content= serializers.CharField()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [ "content", "role" ]


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id", "title", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ConversationDetailSerializer(ConversationSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ["messages"]
