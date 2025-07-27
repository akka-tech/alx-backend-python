from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants__user_id']  # filter by participant

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        other_user_id = request.data.get('other_user_id')
        if not other_user_id:
            return Response({'error': 'other_user_id is required.'}, status=400)

        try:
            other_user = User.objects.get(user_id=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        # Check if a 2-user conversation already exists
        existing = Conversation.objects.filter(participants=request.user).filter(participants=other_user).distinct()
        for convo in existing:
            if convo.participants.count() == 2:
                serializer = self.get_serializer(convo)
                return Response(serializer.data, status=200)

        # Create new conversation
        convo = Conversation.objects.create()
        convo.participants.set([request.user, other_user])
        serializer = self.get_serializer(convo)
        return Response(serializer.data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['sender__user_id']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation__conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_pk']
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionError("Not a participant.")

        serializer.save(sender=self.request.user, conversation=conversation)
