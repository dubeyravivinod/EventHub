from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
@login_required
def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'user/edit_profile.html', {'form': form})

def user_list(request):
    profiles = UserProfile.objects.all()
    return render(request, 'user/user_list.html', {'profiles': profiles})

def user_detail(request, pk):
    profile = UserProfile.objects.get(pk=pk)
    return render(request, 'user/user_detail.html', {'profile': profile})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')
        if form.is_valid():
            user = form.save()
            if email:
                user.email = email
                user.save()
            # create a related profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created and logged in.')
            return redirect('reservation:reservation_list')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('reservation:reservation_list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return redirect('user:login')

