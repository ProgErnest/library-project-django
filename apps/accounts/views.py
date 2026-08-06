from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import RegisterForm, UserProfileForm
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('get_all_books')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, _("Inscription réussie, bienvenue !"))
            return redirect('get_all_books')

    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profil mis à jour avec succès !"))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, "accounts/profile.html", {"form": form})