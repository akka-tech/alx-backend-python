from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()          # Deletes user and cascades related data
        logout(request)        # Logs out the user
        messages.success(request, "Your account and related data have been deleted.")
        return redirect('home')  # Change 'home' to your homepage URL name

    # If GET request, show confirmation page
    return render(request, 'messaging/delete_user_confirm.html')
