from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import User, Hike, Report, Photo, Profile
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


def reports_show(request, report_id):
    report = Report.object.get(id=report_id)
    user = User.object.get(id=report.user_id)
    auth_user = User.objects.get(id=request.user.id)
    photos = Photo.objects.all()
    context = {'report': report, 'user': user,
               'auth_user': auth_user, 'photos': photos}
    return render(request, 'allReports.html', context)


def profile(request):
    user = User.objects.get(id=request.user.id)
    if Profile.objects.filter(user_id=request.user.id):
        profile = Profile.objects.get(user_id=request.user.id)
    else:
        profile = ""
    reports = Report.objects.filter(user=request.user)
    context = {'profile': profile,
               'user': user, 'reports': reports}
    return render(request, 'profile.html', context)


def all_hikes(request):
    hike_all = Hike.objects.all()
    user = User.objects.get(id=request.user.id)
    photos = Photo.objects.all()
    context = {
        'hike_all': hike_all, 'user': user, 'photos': photos}
    return render(request, 'map.html', context)


def hike_show(request, hike_id):
    hike = Hike.objects.get(id=hike_id)
    hike_id = Hike.objects.get(id=hike_id)
    reports = Report.objects.filter(hike_id=hike_id)
    user = User.objects.get(id=request.user.id)
    photos = Photo.objects.all()
    context = {'reports': reports, 'hike': hike, 'hike_id': hike_id,
               'user': user, 'photos': photos}
    return render(request, 'Hikes/hikeShow.html', context)


def report_create(request, hike_id):
    if request.method == 'POST':
        report_form = Report_Form(request.POST)
        print(report_form.errors)
        if report_form.is_valid():
            new_report = report_form.save(commit=False)
            new_report.user = request.user
            new_report.hike_id = hike_id
            new_report.save()
            return redirect('hike_show', hike_id=hike_id)

    # report_form = Report_Form()
    # context = {'report_form': report_form, 'hike_id': hike_id}
    return redirect('all_hikes')
