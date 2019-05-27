from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from .models import Room, RoomAsset, Appointment
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from . import forms


def home_view(request):
    upcoming = Appointment.objects.all()
    upcoming = upcoming.order_by('time')[:5]

    return render(request, 'home.html', {'u_apts': upcoming})


def room_view(request):
    form = None

    if request.method == 'POST':
        form = forms.NewRoomForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            # print(data)

            if data['has_tv'] == '1':
                tv = True
            elif data['asset_type'] == '2':
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

    else:
        form = forms.NewRoomForm()

    return render(request, 'room.html', {'form': form, 'rooms': Room.objects.all()})


def login_view(request):
    form = None

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user = authenticate(
                username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))

    else:
        form = forms.LoginForm()

    return render(request, 'login.html', {'form': form})


def new_user_view(request):
    form = None

    if request.method == 'POST':
        form = forms.CreateNewUserForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            if data['status'] == '1':
                User.objects.create_user(first_name=data['name'], username=data['username'],
                                         password=data['password'], is_staff=True)

            elif data['status'] == '2':
                User.objects.create_user(first_name=data['name'], username=data['username'],
                                         password=data['password'], is_staff=False)
    else:
        form = forms.CreateNewUserForm()

    return render(request, 'generic_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def appointment_details(request, apt_id):
    apt = Appointment.objects.get(id=apt_id)
    return render(request, 'details.html', {'apt': apt})


@login_required(login_url='/login')
def new_appointment(request, room_id):
    form = None
    if request.user.is_authenticated:
        logged_in_user = request.user

    if request.method == 'POST':
        form = forms.NewAppointmentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            room = Room.objects.get(id=room_id)

            new_date = datetime.combine(data['date'], data['time'])

            Appointment.objects.create(time=new_date,
                                       duration=data['duration'],
                                       scheduler=logged_in_user,
                                       room=room)

            return HttpResponseRedirect(reverse('myappointments'))
    else:
        form = forms.NewAppointmentForm()

    return render(request, 'new_appointment.html', {'form': form})


@login_required(login_url='/login')
def my_appointments(request):
    apts = Appointment.objects.filter(scheduler=request.user)
    return render(request, 'myappointments.html', {'apts': apts})
