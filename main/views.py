from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import data
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def home(request):
    if request.method=='POST':
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        email=request.POST["email"]
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'E=mail taken')
                return redirect('')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print("User Created!")
                return redirect('dob')
        else:
            messages.info(request,'Passwords do not match')
            return redirect('register')
        
    else:
        return render(request,'register.html')
    
def success(request):
    return HttpResponse("Created successfully!")

def dob(request):
    if request.method=='POST':
        name=request.POST["name"]
        dob = request.POST["dob"]
        phone = request.POST["phone"]
            
        if User.objects.filter(username=name).exists():
            if data.objects.filter(name=name).exists():
                messages.info(request,'Credentials of this user already entered!')
                return redirect('dob')
            else:
                add_data = data(dob=dob,name=name,phone=phone)
                add_data.save()
            
                credentials = pickle.load(open("C:\\Users\\ACER\\iQube\\firstproject\\main\\token.pkl","rb"))

                service = build("calendar","v3",credentials=credentials)
                result = service.events().list(calendarId="gokulraamkbs6@gmail.com").execute()

                start_time = datetime.now()
                end_time = start_time + timedelta(hours=1)
                timezone = 'Asia/Kolkata'
                event = {
                'summary': 'Birthday of a client',
                'location': 'iQube',
                'description': 'Today is the birthday of an user. No worries when you have an automated mail!',
                'start': {
                    'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'recurrence': [
                    'RRULE:FREQ=YEARLY;COUNT=57'
                ],
                'attendees': [
                    {'email': 'gokul1.19cs@kct.ac.in'},
                    {'email': 'gokulraamofficial@gmail.com'},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
                }

                service.events().insert(calendarId="gokulraamkbs6@gmail.com", body = event).execute()
                return redirect('success')
        else:
            messages.info(request,'Username not found')
            return redirect('dob')
    else:
        return render(request,'dob.html')
    
def send(request):
    now = datetime.now()
    a = now.strftime("%m-%d")
    datas = data.objects.all()
    print(a)
    for dat in datas:
        b = dat.dob.strftime("%m-%d")
        print(b)
        if str(b) == str(a):
            name = dat.name
            subject = 'Happy birthday dear user!'
            message = 'We wish you an amazing birthday ' + name
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['gokulraamofficial@gmail.com',] #I have given only my mail for testing purpose
            send_mail( subject, message, email_from, recipient_list )
    return redirect('/')