import uuid
from django.db import models

# Create your models here.
class User(models.Model):
        USER_ROLES = (
            ('guest', 'Guest'),
            ('host', 'Host'),
            ('admin', 'Admin'),
        )
   
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(null=True)
    last_name = models.CharField(null=True)
    email = models.EmailField(unique=True,null=False)
    password_hash = models.CharField(null=False)
    phone_number = models.CharField(null=True)
    role = models.CharField(choices=USER_ROLES, default='guest' , null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = modeis.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

class Constraints(models.Model):
    