from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

@login_required
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        user.delete()  # triggers cascade & post_delete signal
        logout(request)
        messages.success(request, "Your account and all related data have been deleted.")
        return redirect('home')  # replace 'home' with your homepage url name
    # Render confirmation page
    return render(request, 'messaging/delete_user_confirm.html')
