from django import forms
from django.contrib.auth.models import User


user_status_choices = [('1', 'Staff'), ('2', 'Student')]
tv_choices = [('1', 'Yes'), ('2', 'No')]
asset_choices = [('1', 'Apple TV'), ('2', 'Daily.Co')]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput())


class CreateNewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'password', 'is_staff']


class NewRoomForm(forms.Form):
    name = forms.CharField(max_length=20)
    floor = forms.IntegerField(max_value=4)
    has_tv = forms.ChoiceField(required=True, choices=tv_choices)
    asset_type = forms.ChoiceField(choices=asset_choices)
    asset_name = forms.CharField(max_length=20)
    asset_url = forms.URLField()


class NewAppointmentForm(forms.Form):
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    date = forms.DateField()
    duration = forms.IntegerField(max_value=2)
