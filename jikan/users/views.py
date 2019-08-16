from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.views import generic
from .forms import CustomUserCreationForm
from .models import CustomUser


def signup(request):
    print('request method', request.method)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = CustomUser.objects.create(username=form.cleaned_data['email'], 
                                             email=form.cleaned_data['email'], 
                                             password= form.cleaned_data['password1'],
                                             first_name= form.cleaned_data['first_name'],
                                             last_name = form.cleaned_data['last_name'] )
            # user.username = form.cleaned_data['email']
            # user.email = form.cleaned_data['email']
            user.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.email, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        print('empty user form')
    return render(request, 'signup.html', {'form': form})