from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get email
        password = request.POST.get('password')  # Get password
        
        # Authenticate with email and password
        user = authenticate(request, username=email, password=password)
        
        # Debugging: Print POST data and email/password values
        print("POST Data:", request.POST)
        print("Email:", email)
        print("Password:", password)
        
        if user is not None:  # If authentication is successful
            login(request, user)  # Log the user in
            # Redirect to your dashboard or admin page
            return redirect('admin')  # Replace 'admin' with your desired route name
        else:
            messages.error(request, 'Invalid credentials')  # Display error message
    return render(request, 'authentication/login.html')  # Return the login page
    # authentication/views.py

def admin_view(request):
    return render(request, 'authentication/admin.html')
