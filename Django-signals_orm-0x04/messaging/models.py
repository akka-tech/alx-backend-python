from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    unread = UnreadMessagesManager()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='edited_messages'
    )

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID {self.message.id} at {self.edited_at}"

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if instance.pk:  # Only for updates
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            # Log history before content is updated
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            instance.edited = True  # Mark as edited



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID {self.message.id} at {self.edited_at}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='message_histories')
# messaging/models.py


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # ✅ Add this line to support replies
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.sender} ➝ {self.receiver}: {self.content[:30]}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # <-- NEW
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    objects = models.Manager()  # Default manager
    unread = None  # Will override this in step 2

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'

class Message(models.Model):
    ...
    unread = UnreadMessagesManager()  # Use this for unread filtering

@login_required
def inbox_unread(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {'unread_messages': unread_messages})