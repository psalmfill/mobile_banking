
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from .models import CustomUser
from .facial_recognition import verify_face
from django.core.files.base import ContentFile
import base64
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            
            profile_picture_data = request.POST.get('profile_picture_data')
            if profile_picture_data:
                format, imgstr = profile_picture_data.split(';base64,')
                ext = format.split('/')[-1]
                user.profile_picture = ContentFile(base64.b64decode(imgstr), name=f'{user.username}.{ext}')
            
            user.save()
            
            # Authenticate and log in the user
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                logger.info(f'User {user.username} registered and logged in successfully.')
                # return redirect('dashboard')
                return render(request, 'dashboard.html')

            else:
                logger.error(f'Failed to authenticate user {user.username} after registration.')
                return render(request, 'error.html')  # Redirect to an error page if login fails
        else:
            logger.error(f'Registration form is invalid: {form.errors}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save(commit=False)
#             profile_picture_data = request.POST.get('profile_picture_data')
#             if profile_picture_data:
#                 format, imgstr = profile_picture_data.split(';base64,')
#                 ext = format.split('/')[-1]
#                 user.profile_picture = ContentFile(base64.b64decode(imgstr), name=f'{user.username}.{ext}')
#             user.save()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            profile_picture_data = request.POST.get('profile_picture_data')
            if verify_face(user.profile_picture.path, profile_picture_data):
                login(request, user)
                return redirect('dashboard')
    return render(request, 'registration/login.html')

def facial_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = CustomUser.objects.filter(username=username).first()
        if user:
            profile_picture_data = request.POST.get('profile_picture_data')
            if verify_face(user.profile_picture.path, profile_picture_data):
                login(request, user)
                return redirect('dashboard')
    return render(request, 'registration/facial_login.html')


def dashboard(request):
    return render(request, 'dashboard.html')
