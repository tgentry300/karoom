from django.views import View
from django.contrib.auth.models import User
from .models import Room, RoomAsset, Appointment
from django.contrib.auth import login, authenticate
from django.shortcuts import render, HttpResponseRedirect, reverse
from datetime import datetime
from . import forms


class RoomView(View):
    form_class = forms.NewRoomForm
    template = 'room.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form, 'rooms': Room.objects.all()})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if data['has_tv'] == '1':
                tv = True
            elif data['has_tv'] == '2':
                tv = False

            if data['asset_type'] == '1':
                asset_type = 'Apple TV'
            elif data['asset_type'] == '2':
                asset_type = 'Daily.co'

            new_asset = RoomAsset.objects.create(asset_name=data['asset_name'],
                                                 asset_type=asset_type,
                                                 url=data['asset_url'])

            Room.objects.create(name=data['name'],
                                floor=data['floor'],
                                has_tv=tv, assets=new_asset)

        return render(request, self.template, {'form': form, 'rooms': Room.objects.all()})


class LoginView(View):
    form_class = forms.LoginForm
    template = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(
                username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/myappointments'))


class NewUserView(View):
    form_class = forms.CreateNewUserForm
    template = 'generic_form.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = User.objects.create_user(first_name=data['first_name'], username=data['username'],
                                            password=data['password'], is_staff=data['is_staff'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))


class NewAppointmentView(View):
    form_class = forms.NewAppointmentForm
    template = 'new_appointment.html'

    def get(self, request, room_id):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request, room_id):
        form = self.form_class(request.POST)
        logged_in_user = None

        if request.user.is_authenticated:
            logged_in_user = request.user

        if form.is_valid():
            data = form.cleaned_data

            room = Room.objects.get(id=room_id)
            # maybe try to use timezone from django
            new_date = datetime.combine(data['date'], data['time'])

            Appointment.objects.create(
                time=new_date,
                duration=data['duration'],
                scheduler=logged_in_user,
                room=room
            )

            return HttpResponseRedirect(reverse('myappointments'))
