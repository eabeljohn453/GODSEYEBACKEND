from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/auth/admin/')  
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "authentication/login.html")

@login_required(login_url='/auth/login')
@never_cache
def admin_view(request):
    return render(request, "authentication/admin.html")

def logout_view(request):
    logout(request)
    return redirect('/auth/login/')
