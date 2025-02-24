from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import CustomUser  # Ensure CustomUser extends AbstractUser

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Fetch email from form
        password = request.POST.get('password')

        print(f"Attempting login for: {email}")  # Debugging
        user = authenticate(request, username=email, password=password)  # Change username → email

        if user is not None:
            print(f"Login successful for: {user.username}, Type: {user.user_type}")  # Debugging
            login(request, user)

            if user.user_type == 'admin':
                return redirect('/auth/admin/')
            else:
                return redirect('/auth/user/')
        else:
            print("Login failed: Invalid credentials")  # Debugging
            messages.error(request, "Invalid username or password")

    return render(request, 'authentication/login.html')
@login_required(login_url='login')  # Ensure only logged-in users can access
@never_cache
def admin_view(request):
    if request.user.user_type != 'admin':
        messages.error(request, "Access denied. Admins only.")
        return redirect('user_dashboard')

    return render(request, 'authentication/admin.html')

@login_required(login_url='login')
@never_cache
def user_view(request):
    if request.user.user_type != 'user':  # Ensure only users can access
        return redirect('/auth/admin/')  
    return render(request, 'authentication/user.html')  # Match the folder structure


def logout_view(request):
    logout(request)  # Log out user properly
    return redirect('login')  # Redirect to login page correctly
