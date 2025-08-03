from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()         
        logout(request)        
        messages.success(request, "Your account and related data have been deleted.")
        return redirect('home')  

    return render(request, 'messaging/delete_user_confirm.html')
