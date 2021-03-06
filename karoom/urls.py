"""karoom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views, class_views

handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('rooms', class_views.RoomView.as_view()),
    path('login', class_views.LoginView.as_view()),
    path('newuser', class_views.NewUserView.as_view()),
    path('logout', views.logout_view),
    path('myappointments', views.my_appointments, name='myappointments'),
    path('schedule/<int:room_id>', login_required(class_views.NewAppointmentView.as_view(), login_url='/login')),
    path('details/<int:apt_id>', views.appointment_details)
]
