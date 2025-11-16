# messaging_app/chats/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages__sender")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a conversation by passing 'participant_ids': [id1, id2, ...]
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conv = serializer.save()
        return Response(self.get_serializer(conv).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a message. Payload example:
        {
          "conversation": "<conversation_uuid>",
          "message_body": "Hello"
        }
        Sender is taken from request.user if authenticated, else must provide 'sender_id' in payload.
        """
        sender = None
        if request.user and request.user.is_authenticated:
            sender = request.user
        else:
            sender_id = request.data.get("sender_id")
            if not sender_id:
                return Response({"detail": "Sender not provided"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                sender = User.objects.get(user_id=sender_id)
            except User.DoesNotExist:
                return Response({"detail": "Sender not found"}, status=status.HTTP_400_BAD_REQUEST)

        conversation_id = request.data.get("conversation")
        if not conversation_id:
            return Response({"detail": "Conversation id required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conv = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            sender=sender,
            conversation=conv,
            message_body=request.data.get("message_body", "")
        )
        return Response(self.get_serializer(message).data, status=status.HTTP_201_CREATED)
