from django.shortcuts import render
from .models import Appointment
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home_view(request):
    upcoming = Appointment.objects.all()
    upcoming = upcoming.order_by('time')[:5]
    return render(request, 'home.html', {'u_apts': upcoming})


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def appointment_details(request, apt_id):
    apt = Appointment.objects.get(id=apt_id)
    return render(request, 'details.html', {'apt': apt})


@login_required(login_url='/login')
def my_appointments(request):
    apts = Appointment.objects.filter(scheduler=request.user)
    return render(request, 'myappointments.html', {'apts': apts})
