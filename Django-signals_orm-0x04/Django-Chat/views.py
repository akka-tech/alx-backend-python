from django.shortcuts import render
from .models import Message
from .utils import build_threaded_messages  # move the function here if needed

def inbox_view(request):
    user = request.user
    all_messages = Message.objects.filter(receiver=user) \
        .select_related('sender', 'receiver', 'parent_message') \
        .prefetch_related('replies__sender', 'replies__receiver')

    threads = build_threaded_messages(all_messages)
    return render(request, 'messaging/inbox.html', {'threads': threads})