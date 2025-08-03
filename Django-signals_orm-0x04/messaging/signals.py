from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_old_content_before_update(sender, instance, **kwargs):
    if not instance.pk:
        # This is a new message, no old content to log
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # The message does not exist in DB yet
        return

    if old_message.content != instance.content:
        # Log the old content before update
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        instance.edited = True
