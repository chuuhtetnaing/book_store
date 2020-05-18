from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, ChangeUserPasswordForm
from store.models import Book
from django.conf import settings
from surprise import dump
import os

_, cf_user_to_user = dump.load(os.path.join(settings.BASE_DIR, 'cf_user_to_user.sav'))

user_ac5 = [22465085,
 18775169,
 11543195,
 11275,
 15751404,
 2570856,
 14817,
 13055592,
 13603717,
 39242,
 88071,
 51964,
 13453029]

user_7b2 = [2981076, 29056083, 3876]

# Create your views here.

def home(request):
    return render(request, 'account/home.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome!"))
            return redirect('account:home')
        else:
            messages.success(request, ("Error Logging In - Please Try Again"))
            return redirect('account:login')
    else:
        return render(request, 'account/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You Have Been Logget Out.'))
    return redirect('account:home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password= password)
            login(request, user)
            messages.success(request, ("You Have Registered!"))
            return redirect('account:home')
    else:
        form = SignUpForm()

    context = {'form': form}
    return  render(request, 'account/register.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("You Have Successfully Edited Your Profile!"))
            return redirect('account:home')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'account/edit_profile.html', context)

def purchase_history(request):
    history = list()
    recommendation = list()
    if (request.user.is_authenticated) and (request.user.username == 'ac5b887c1d04bbfe9bbc8ce4b8f968be'):
        for id in user_ac5:
            history.append(Book.objects.get(book_id=id))
        for id in [predicted[0] for predicted in cf_user_to_user[request.user.username]]:
            recommendation.append(Book.objects.get(book_id=id))
    elif (request.user.is_authenticated) and (request.user.username == '7b2a80e516033af7b8f1a11d29067f4e'):
        for id in user_7b2:
            history.append(Book.objects.get(book_id=id))
        for id in [predicted[0] for predicted in cf_user_to_user[request.user.username]]:
            recommendation.append(Book.objects.get(book_id=id))
    else:
        history = None


    context = {'purchase_history': history, 'user_to_user_recommendation_books': recommendation}
    return render(request, 'account/purchase_history.html', context)

def guide(request):
    context = {}
    return render(request, 'account/guide.html', context)

def change_password(request):
    if request.method == 'POST':
        form = ChangeUserPasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ("You Have Successfully Edited Your Password!"))
            return redirect('account:home')
    else:
        form = ChangeUserPasswordForm(user=request.user)

    context = {'form': form}
    return render(request, 'account/change_password.html', context)