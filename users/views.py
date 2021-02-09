from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)                                # Instantiate the form
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,                              # authenticate the user against the database
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})













# from django.contrib.auth import login
# from django.shortcuts import render, redirect
# from django.urls import reverse
# from users.forms import CustomUserCreationForm
#
#
# def dashboard(request):
#     return render(request, "users/dashboard.html")
#
#
# def register(request):
#     if request.method == "GET":
#         return render(
#             request, "users/register.html",
#             {"form": CustomUserCreationForm}
#         )
#     elif request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect(reverse("dashboard"))
