from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
import json


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session["username"] = user.username
            messages.success(request, f"Welcome back, {username}!")
            
            # Redirect to 'next' parameter if provided, otherwise go to home
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('user_login')

    return render(request, "login.html")


@csrf_exempt
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        
        # Validation: Check if all fields are filled
        has_errors = False
        
        if not username:
            messages.error(request, "Username is required.")
            has_errors = True
        elif len(username) < 3:
            messages.error(request, "Username must be at least 3 characters.")
            has_errors = True
        
        if not email:
            messages.error(request, "Email is required.")
            has_errors = True
        elif "@" not in email or "." not in email:
            messages.error(request, "Please enter a valid email address.")
            has_errors = True
        
        if not password:
            messages.error(request, "Password is required.")
            has_errors = True
        elif len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            has_errors = True
        
        # Check if username already exists (only if basic validation passed)
        if not has_errors and User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            has_errors = True
        
        # Check if email already exists (only if basic validation passed)
        if not has_errors and User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use another email.")
            has_errors = True
        
        # If there are errors, redirect back to register page
        if has_errors:
            return redirect("user_register")
        
        # Create user and log them in
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            login(request, user)
            request.session["username"] = user.username
            messages.success(request, f"Welcome {username}! Your account has been created successfully.")
            return redirect("home")
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {str(e)}")
            return redirect("user_register")

    return render(request, "register.html")


@csrf_exempt
def check_username_availability(request):
    """
    AJAX endpoint to check if username is available.
    Returns JSON response with availability status.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            
            if not username:
                return JsonResponse({'available': False, 'message': 'Username is required.'})
            
            if len(username) < 3:
                return JsonResponse({'available': False, 'message': 'Username must be at least 3 characters.'})
            
            # Check if username exists
            exists = User.objects.filter(username=username).exists()
            
            if exists:
                return JsonResponse({'available': False, 'message': 'Username already taken.'})
            else:
                return JsonResponse({'available': True, 'message': 'Username is available!'})
        
        except json.JSONDecodeError:
            return JsonResponse({'available': False, 'message': 'Invalid request.'})
    
    return JsonResponse({'available': False, 'message': 'Invalid request method.'})


@csrf_exempt
def check_email_availability(request):
    """
    AJAX endpoint to check if email is available.
    Returns JSON response with availability status.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            
            if not email:
                return JsonResponse({'available': False, 'message': 'Email is required.'})
            
            # Simple email format validation
            if '@' not in email or '.' not in email:
                return JsonResponse({'available': False, 'message': 'Please enter a valid email address.'})
            
            # Check if email exists
            exists = User.objects.filter(email=email).exists()
            
            if exists:
                return JsonResponse({'available': False, 'message': 'Email already registered.'})
            else:
                return JsonResponse({'available': True, 'message': 'Email is available!'})
        
        except json.JSONDecodeError:
            return JsonResponse({'available': False, 'message': 'Invalid request.'})
    
    return JsonResponse({'available': False, 'message': 'Invalid request method.'})


@csrf_exempt
def user_logout(request):
    """Log out the user and redirect to clean homepage"""
    logout(request)
    # Clear all session data for clean state
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")
