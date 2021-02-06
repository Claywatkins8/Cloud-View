from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import User, Hike, Report, Photo
from .forms import NewUserForm, Report_Form

from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
# Define the home view


def home(request):
    error_message = ''
    if request.method == 'POST':
        signup_form = NewUserForm(request.POST)
        username_form = request.POST['username']
        email_form = request.POST['email']
        if User.objects.filter(username=username_form).exists():
            context = {'error': 'Username is already taken'}
            return render(request, 'home.html', context)
        else:
            if User.objects.filter(email=email_form).exists():
                context = {'error': 'That email is already taken'}
                return render(request, 'home.html', context)
            else:
                if signup_form.is_valid():
                    user = signup_form.save()
                    user.save()
                    login(request, user)
                    return redirect('home/')
                else:
                    context = {'error': 'Invalid signup, please try again!'}
                    return render(request, 'home.html', context)

    signup_form = NewUserForm()
    login_form = AuthenticationForm()
    context = {'signup_form': signup_form, 'login_form': login_form, }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def all_map(request):
    return render(request, 'map.html')


def reports_show(request):
    return render(request, 'allReports.html')
