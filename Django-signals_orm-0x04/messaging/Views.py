# messaging/views.py

from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required

def build_threaded_messages(messages_queryset):
    messages = list(messages_queryset)
    message_map = {msg.id: msg for msg in messages}
    for msg in messages:
        msg.children = []
    root_messages = []
    for msg in messages:
        if msg.parent_message_id:
            parent = message_map.get(msg.parent_message_id)
            if parent:
                parent.children.append(msg)
        else:
            root_messages.append(msg)
    return root_messages

@login_required
def threaded_conversations(request):
    all_messages = Message.objects.filter(receiver=request.user) \
        .select_related('sender', 'receiver', 'parent_message') \
        .prefetch_related('replies__sender', 'replies__receiver')

    threads = build_threaded_messages(all_messages)
    return render(request, 'messaging/threaded_view.html', {'threads': threads})
