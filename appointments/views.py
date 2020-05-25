from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .models import Appointment
from datetime import datetime
from django.utils import timezone
from home.context_processors import hasGroup
from case.models import case
from django.contrib import messages
# Create your views here.

#CREATE
@login_required
def book(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        c = {}
        c.update(csrf(request))
        c['patients'] = User.objects.filter(groups__name='patient')
        c['doctors'] = User.objects.filter(groups__name='doctor')
        c['cases'] = case.objects.all()
        return render(request, 'appointments/book_appointment.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def doBook(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        patient = User.objects.get(username=request.POST.get('patient', ''))
        doctor = User.objects.get(username=request.POST.get('doctor', ''))
        c = case.objects.get(pk=int(request.POST.get('case', '')))
        appointment_time = request.POST.get('appointment_date')+'T'+request.POST.get('appointment_time')
        appointment_time = datetime(*[int(v) for v in appointment_time.replace('T', '-').replace(':', '-').split('-')])
        appointment = Appointment(patient=patient, doctor=doctor, receptionist=request.user, case=c, appointment_time=appointment_time)
        appointment.save()
        messages.add_message(request, messages.INFO, 'Appointment Successfully Booked')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/appointments/')


#RETRIEVE
@login_required
def view(request):
    c = {}
    user = request.user
    if hasGroup(user, 'receptionist'):
        c['isReceptionist'] = True
        c['appointments'] = Appointment.objects.filter(appointment_time__gte=timezone.now()).order_by('appointment_time')
    elif hasGroup(user, 'patient'):
        c['appointments'] = Appointment.objects.filter(patient=user, appointment_time__gte=timezone.now()).order_by('appointment_time')
    elif hasGroup(user, 'doctor'):
        c['appointments'] = Appointment.objects.filter(doctor=user, appointment_time__gte=timezone.now()).order_by('appointment_time')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')
    return render(request, 'appointments/view_all.html', c)


#UPDATE
@login_required
def changeAppointment(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        c = {'appointment': Appointment.objects.get(pk=id)}
        c['doctors'] = User.objects.filter(groups__name='doctor')
        c.update(csrf(request))
        return render(request, 'appointments/change.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def doChange(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        appointment = Appointment.objects.get(pk=int(request.POST.get('id')))
        appointment.doctor = User.objects.get(username=request.POST.get('doctor', ''))
        appointment_time = request.POST.get('appointment_date')+'T'+request.POST.get('appointment_time')
        appointment_time = datetime(*[int(v) for v in appointment_time.replace('T', '-').replace(':', '-').split('-')])
        appointment.appointment_time = appointment_time
        appointment.receptionist = request.user
        appointment.save()
    messages.add_message(request, messages.INFO, 'Appointment Successfully Changed')
    return HttpResponseRedirect('/appointments/')

#DELETE
def delete(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        Appointment.objects.get(id=id).delete()
        messages.add_message(request, messages.INFO, 'Appointment Successfully Deleted')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/appointments/')
