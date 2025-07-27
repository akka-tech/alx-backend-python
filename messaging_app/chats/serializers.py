# chats/serializers.py

from rest_framework import serializers
from .models import User, Message, Conversation  # Ensure Message & Conversation are imported


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    # SerializerMethodField example: Count total messages in a conversation
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'message_count']
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        return obj.message_set.count()  # assumes related_name='message_set' on Message.conversation


class MessageSerializer(serializers.ModelSerializer):
    # SerializerMethodField example: full sender name
    sender_name = serializers.SerializerMethodField()
    # CharField example (not tied to model): optional echo field for testing
    echo = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'sender_name', 'echo']
        read_only_fields = ['message_id', 'sent_at', 'sender_name']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty or whitespace.")
        return value
