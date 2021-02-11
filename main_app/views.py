from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import User, Hike, Report, userPhoto, hikePhoto, reportPhoto
from .forms import NewUserForm, Report_Form


# AWS IMPORTS
import boto3
import uuid
# AWS "Constants"
S3_BASE_URL = 'https://s3-us-west-2.amazonaws.com/'
BUCKET = 'cloud-view'
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
                    return redirect('/')
                else:
                    context = {'error': 'Invalid signup, please try again!'}
                    return render(request, 'home.html', context)
    reports = Report.objects.all().order_by('-id')[:3]
    signup_form = NewUserForm()
    login_form = AuthenticationForm()
    userphoto = userPhoto.objects.all()
    hikephoto = hikePhoto.objects.all()
    reportphoto = reportPhoto.objects.all()
    context = {'reports': reports, 'signup_form': signup_form,
               'login_form': login_form, 'userphoto': userphoto, 'hikephoto': hikephoto, 'reportphoto': reportphoto}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def reports_all(request):
    reports = Report.objects.all()
    userphoto = userPhoto.objects.all()
    hikephoto = hikePhoto.objects.all()
    reportphoto = reportPhoto.objects.all()
    context = {'reports': reports,
               'userphoto': userphoto, 'hikephoto': hikephoto, 'reportphoto': reportphoto}
    return render(request, 'allReports.html', context)


@login_required
def reports_show(request, report_id):
    report = Report.objects.get(id=report_id)
    user = User.objects.get(id=report.user_id)
    auth_user = User.objects.get(id=request.user.id)
    userphoto = userPhoto.objects.all()
    hikephoto = hikePhoto.objects.all()
    reportphoto = reportPhoto.objects.filter(report_id=report_id)
    context = {'report': report, 'user': user,
               'auth_user': auth_user, 'userphoto': userphoto, 'hikephoto': hikephoto, 'reportphoto': reportphoto}
    return render(request, 'Reports/show.html', context)


@login_required
def reports_edit(request, report_id):
    report = Report.objects.get(id=report_id)
    if request.user == report.user:
        if request.method == 'POST':
            report_form = Report_Form(request.POST, instance=report)
            if report_form.is_valid():
                report_form.save()
                return redirect('reports_show', report_id=report.id)

    # report_form = Report_Form(instance=report)
    # context = {'report_form': report_form, 'report': report}
    # return render(request, 'Reports/show.html', context)
    return redirect('/profile/')


@login_required
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


@login_required
def report_delete(request, report_id, hike_id):
    item = Report.objects.get(id=report_id)
    if request.user == item.user:
        Report.objects.get(id=report_id).delete()
        return redirect('profile')
    else:
        return redirect('hike_show', hike_id=hike_id)


@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    reports = Report.objects.filter(user=request.user)
    userphoto = userPhoto.objects.filter(user=request.user)
    hikephoto = hikePhoto.objects.all()
    reportphoto = reportPhoto.objects.all()
    context = {
        'user': user, 'reports': reports, 'userphoto': userphoto, 'hikephoto': hikephoto, 'reportphoto': reportphoto}
    return render(request, 'profile.html', context)


def all_hikes(request):
    hike_all = Hike.objects.all()
    userphoto = userPhoto.objects.all()
    hikephoto = hikePhoto.objects.all()
    context = {
        'hike_all': hike_all, 'userphoto': userphoto, 'hikephoto': hikephoto, }
    return render(request, 'map.html', context)


def hike_show(request, hike_id):
    hike = Hike.objects.get(id=hike_id)
    hike_id = Hike.objects.get(id=hike_id)
    reports = Report.objects.filter(hike_id=hike_id)
    userphoto = userPhoto.objects.all()
    hikephoto = hikePhoto.objects.all()
    reportphoto = reportPhoto.objects.all()
    context = {'reports': reports, 'hike': hike, 'hike_id': hike_id,
               'userphoto': userphoto, 'hikephoto': hikephoto, 'reportphoto': reportphoto, }
    return render(request, 'Hikes/hikeShow.html', context)


@login_required
def add_user_photo(request):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = userPhoto(url=url,
                              user_id=request.user.id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile')


@login_required
def add_report_photo(request, report_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = reportPhoto(url=url, report_id=report_id,
                                user_id=request.user.id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('reports_all')


@login_required
def add_hike_photo(request, hike_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = hikePhoto(url=url, hike_id=hike_id,
                              user_id=request.user.id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('home')


@login_required
def user_photo_delete(request, photo_id):
    userPhoto.objects.get(id=photo_id).delete()
    return redirect('profile')


@login_required
def report_photo_delete(request, photo_id):
    reportPhoto.objects.get(id=photo_id).delete()
    return redirect('home')


@login_required
def hike_photo_delete(request, photo_id):
    hikePhoto.objects.get(id=photo_id).delete()
    return redirect('home')
