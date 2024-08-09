from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            return redirect('home') 
        
    return render(request, 'login.html')

@csrf_exempt
def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        login(request, user)
        return redirect('home') 

    return render(request, 'register.html')

@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect('home')



