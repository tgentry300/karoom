from django import forms
from .models import Room


user_status_choices = [('1', 'Staff'), ('2', 'Student')]
tv_choices = [('1', 'Yes'), ('2', 'No')]
asset_choices = [('1', 'Apple TV'), ('2', 'Daily.Co')]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput())


class CreateNewUserForm(forms.Form):
    name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    status = forms.ChoiceField(required=True, choices=user_status_choices)


class NewRoomForm(forms.Form):
    name = forms.CharField(max_length=20)
    floor = forms.IntegerField(max_value=4)
    has_tv = forms.ChoiceField(required=True, choices=tv_choices)
    asset_type = forms.ChoiceField(choices=asset_choices)
    asset_name = forms.CharField(max_length=20)
    asset_url = forms.URLField()


class NewAppointmentForm(forms.Form):
    time = forms.DateTimeField()
    duration = forms.IntegerField(max_value=2)
    room = forms.ModelChoiceField(queryset=Room.objects.all())
