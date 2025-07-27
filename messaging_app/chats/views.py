from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, User
from .serializers import ConversationSerializer
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        current_user = request.user
        other_user_id = request.data.get('other_user_id')

        if not other_user_id:
            return Response({'error': 'other_user_id is required.'}, status=400)

        try:
            other_user = User.objects.get(user_id=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

   
        existing_conversations = Conversation.objects.filter(participants=current_user).filter(participants=other_user).distinct()

        for convo in existing_conversations:
            if convo.participants.count() == 2:
                serializer = self.get_serializer(convo)
                return Response(serializer.data, status=200)

        
        new_convo = Conversation.objects.create()
        new_convo.participants.set([current_user, other_user])
        serializer = self.get_serializer(new_convo)
        return Response(serializer.data, status=201)
