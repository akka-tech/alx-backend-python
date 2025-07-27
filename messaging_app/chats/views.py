from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Show only conversations involving current user
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)  # Add creator as participant


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # messages in a specific conversation
        conversation_id = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation__conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_pk']
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant of this conversation."}, status=403)

        serializer.save(sender=self.request.user, conversation=conversation)
