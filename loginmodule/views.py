from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib import messages
from django.contrib.auth.models import User,Group
from profiles.models import Patient, Doctor

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO,
                             'You are already Logged in.')
        return HttpResponseRedirect('/home')
    else:
        c = {}
        c.update(csrf(request))
        print(c)
        return render(request, 'loginmodule/login.html', c)


def login1(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO,
                             'You are already Logged in.')
        return HttpResponseRedirect('/home')
    else:
        c = {}
        c.update(csrf(request))
        print(c)
        return render(request, 'loginmodule/login1.html', c)

def register(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO,
                             'You are already Logged in.')
        return HttpResponseRedirect('/home')
    else:
        c = {}
        c.update(csrf(request))
        print(c)
        return render(request, 'loginmodule/register.html')

def doRegister(request):
    print("Registering a new User")
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, 'Username Already Exists.')
        return HttpResponseRedirect('/profile/register')
    password = request.POST.get('password1')
    cpassword = request.POST.get('password2')
    if not password == cpassword:
        messages.add_message(request, messages.ERROR, 'Passwords not matching.')
        return HttpResponseRedirect('/profile/register')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    contact_no = request.POST.get('contact_no')
    if not contact_no.isdigit():
        messages.add_message(request, messages.ERROR, 'Wrong Contact no.')
        return HttpResponseRedirect('/profile/register')
    address = request.POST.get('address')
    dob = request.POST.get('dob')
    blood_group = request.POST.get('blood_group')
    typeUser = request.POST.get("type")
    print(typeUser)
    print(type(typeUser))
    email = request.POST.get('email')
    new_user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    print(new_user)
    if typeUser=="Doctor":
        print("Creating a new record for Doctor")
        group = Group.objects.get(name='doctor')
        new_user.doctor = Doctor(contact_no=int(contact_no), address=address, dob=dob, blood_group=blood_group)
        new_user.doctor.save()
        new_user.save()
        print(group)
        group.user_set.add(new_user)
        group.save()
    else:
        print("Creating a new Record for a Patient")
        new_user.patient = Patient(contact_no=int(contact_no), address=address, dob=dob, blood_group=blood_group)
        new_user.patient.save()
        group = Group.objects.get(name='patient')
        new_user.save()
        print(group)
        group.user_set.add(new_user)
        group.save()

    messages.add_message(request, messages.WARNING, 'Successfully Registered '+username)
    return HttpResponseRedirect('/case/generate')

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print("[I] Trying to login with Username : {} and Password {} : ".format(username, password))
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        messages.add_message(request, messages.INFO, 'Your are now Logged in.')
        return HttpResponseRedirect('/home')
    else:
        messages.add_message(request, messages.WARNING,
                             'Invalid Login Credentials.')
        return HttpResponseRedirect('/login')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    messages.add_message(request, messages.INFO,
                         'You are Successfully Logged Out')
    messages.add_message(request, messages.INFO, 'Thanks for visiting.')
    return HttpResponseRedirect('/login')
