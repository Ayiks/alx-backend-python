# messaging_app/chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Expose user_id as id in API or keep user_id
        fields = ("user_id", "username", "first_name", "last_name", "email", "phone_number", "role")


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ("message_id", "sender", "message_body", "sent_at")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, source="participants"
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ("conversation_id", "participants", "participant_ids", "messages", "created_at")

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        conv = Conversation.objects.create()
        if participants:
            conv.participants.set(participants)
        return conv
