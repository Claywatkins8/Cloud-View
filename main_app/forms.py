from django.forms import ModelForm
from .models import User, Report

from django.contrib.auth.forms import UserCreationForm, forms


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class Report_Form(ModelForm):
    class Meta:
        model = Report
        fields = ['hikeType', 'content', 'conditions',
                  'road', 'bugs', 'snow']
