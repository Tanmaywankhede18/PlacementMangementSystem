
from ast import Pass
from contextlib import redirect_stderr
from hashlib import new
from importlib.metadata import requires
from operator import ge
import re
from this import d
from django.http import HttpResponse
from django.shortcuts import redirect, render
from pkg_resources import Requirement
from student.models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.contrib.sites.shortcuts import get_current_site  
from django.core.mail import EmailMessage 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from student.token import account_activation_token  
from django.utils.encoding import force_bytes,force_str
# Create your views here.
import  pandas as pd 

def POdashboard(request):
   
    events = Event.objects.all()
    st = Student.objects.filter(verified=0)
    return render(request,'PMdashboard.html',{'data':events,'students':st})


def index(request):
    if(request.method=="POST"):
        name = request.POST.get("name")
        ctc = request.POST.get("ctc")
        lastdate = request.POST.get("lastdate")
        Requirement = request.POST.get("requirements")
        passouts = request.POST.get("passouts")
        link = request.POST.get("link")
        roll = request.POST.get('roll')
        event = Event(drive_name = name,
        req=Requirement,
        roll=roll,
        ctc=ctc,
        passouts = passouts,
        last_date = lastdate,
        link = link
        )
        event.save()
        

    user = request.user
    try:
        obj = Student.objects.get(user_id=user.id)
    except Student.DoesNotExist:
        return redirect('/student/Register')
    events = Event.objects.all()
    print(events)

    if user.is_staff:
        return redirect('/student/PODashboard')
    
    if obj.verified:
        return render(request, 'dashboard.html',{'data':events})
    else:
        return render(request, 'Verfication.html')   




        
def test(request):

    # if request.method=="POST":
    #     email = request.POST.get('email')
    #     password = request.POST.get('pass')
    #     user = User.objects.create_user(email,email,password);
    #     user.is_active = False  
    #     user.save()  
    #     current_site = get_current_site(request)  
    #     mail_subject = 'Activation link has been sent to your email id'  
    #     message = render_to_string('acc_active_email.html', {  
    #             'user': user,  
    #             'domain': current_site.domain,  
    #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
    #             'token':account_activation_token.make_token(user),  
    #         })  
    #     email = EmailMessage(  
    #                     mail_subject, message, to=[email]  
    #         )  
    #     email.send()  
    #     return HttpResponse('Please confirm your email address to complete the registration')  
    if request.method == "POST":
        filter = request.POST.get('pass')
        name  = request.POST.get('name')
        stu = Student.objects.filter(ug_marks__gte=filter).filter(first_name=name)
        prn  = []
        name = []
        ug = []
        ug_marks  = []
        for s in stu:
            prn.append(s.PRN)
            name.append(str(s.first_name)+str(s.last_name))
            ug.append(s.ug)
            ug_marks.append(s.ug_marks)

        df = pd.DataFrame({'PRN': prn,'Name':name,'Stream':ug,'Marks':ug_marks})
        writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        return render(request,'test.html',{'data':stu})

    stu = Student.objects.all()
    return render(request,'test.html',{'data':stu})

def signout(request):
    logout(request)
    return redirect('/student/Signup')

def signup(request):
    email = request.POST.get('Email')
    a = False
    if email!=None:
            if(User.objects.filter(username=email).exists()):
                print("User already exists")
                a = True
            else:
                Password = request.POST.get('Pass')
                new_user = User.objects.create_user(email,email,Password)
                new_user.save()
                current_site = get_current_site(request)  
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('acc_active_email.html', {  
                'user': new_user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),  
                'token':account_activation_token.make_token(new_user),  
                })  
                email = EmailMessage(  
                                mail_subject, message, to=[email]  
                    )  
                email.send()  
                return HttpResponse('Please confirm your email address to complete the registration')  
    
                return redirect('/student/Register')

    return render(request,'Signup.html',{'message_exist':a})


def register(request):
    if request.user.is_authenticated:
        if Student.objects.filter(user_id=request.user.id):
            print("User Filled his form")

        if request.method=='POST':
            email = request.user.username
            firstname = request.POST.get('first_name')
            middlename = request.POST.get('middle_name')
            lastname = request.POST.get('last_name')
            address = request.POST.get('address')
            birth_date = request.POST.get('birth_date')
            gender = request.POST.get('gender')
            mobile = request.POST.get('mobile')
            prn = request.POST.get('PRN')
            city = request.POST.get('city')
            state = request.POST.get('state')
            ug = request.POST.get('ug')
            ug_marks = request.POST.get('ug_marks')
            ug_passout = request.POST.get('ug_passout')
            ug_stream = request.POST.get('ug_stream')
            deploma = request.POST.get('deploma')
            deploma_marks = request.POST.get('deploma_marks')
            deploma_passout = request.POST.get('deploma_passout')
            deploma_stream = request.POST.get('deploma_stream')
            ssc = request.POST.get('ssc')
            ssc_marks = request.POST.get('ssc_marks')
            ssc_passout  = request.POST.get('ssc_passout')
            
            print(gender,ug_stream,deploma_stream)
            
            stu = Student(
            email = email,
            roll = "student",
            verified = False,
            first_name = firstname,
            middle_name = middlename,
            last_name = lastname,
            birth_date = birth_date,
            gender = gender,
            address = address,
            city = city,
            state = state,
            mobile = mobile,
            PRN = prn,
            ug = ug,
            ug_marks = ug_marks,
            ug_passout =ug_passout,
            ug_stream = ug_stream,
            diploma = deploma,
            diploma_marks = deploma_marks,
            diploma_stream = deploma_stream,
            diploma_passout = deploma_passout,
            school = ssc,
            school_marks = ssc_marks,
            school_passout = ssc_passout,
            user = request.user,
            extra_curriculam = {"Activity 1":'premier legue'}
            )

            stu.save()
            return redirect('/student/dashboard')
        return render(request,'register_div.html')
    else:
        return redirect('/student/Signup')

def TPO(request):
     return render(request, 'TPORegister.html')
# def Register(request):
#     if request.method == 'POST':
#         name = request.POST.get("Name")
#         email = request.POST.get("Email")
#         Dep = request.POST.get("Dep")
#         mobile = request.POST.get("Mobile")
#         Pass = request.POST.get("Pass")
#         RPass = request.POST.get("RPass")
#         if((RPass==Pass)and(RPass!=None)):
#                 new_user = User.objects.create_user(email, email, Pass)
#                 new_user.is_active = False
#                 new_user.first_name = name
#                 new_user.save()
#                 o = Admin(fullname=name,email=email,mobile=mobile,dep=Dep,user=new_user)
#                 o.save()
#                 print("Data Saved Successfully")
#                 return redirect('/student/dashboard')
           
#             # Redirect user to dashboard 
#     return render(request, 'TPORegister.html')


def Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username!=None:
           user = authenticate(username = username,password = password)
           if user.is_active:
                login(request,user)
                if user.is_authenticated:
                        return redirect('/student/dashboard')
           else:
               return HttpResponse('Please confirm your email address to complete the registration')    
               
    return render(request,'Login.html')


def activate(request, uidb64, token):  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        login(request,user)
        if user.is_authenticated:
                return redirect('/student/dashboard')
         
    else:  
        return HttpResponse('Activation link is invalid!')  

def Filter(request):
    stu = Student.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        prn = request.POST.get('PRN')
        dep = request.POST.get('Dep')
        marks = request.POST.get('marks')
        skills = request.POST.get('skills')
    
        stu = Student.objects.filter(ug_marks__gte=marks).filter(first_name=name)
        prn  = []
        name = []
        ug = []
        ug_marks  = []


        for s in stu:
            prn.append(s.PRN)
            name.append(str(s.first_name)+str(s.last_name))
            ug.append(s.ug)
            ug_marks.append(s.ug_marks)

        

        df = pd.DataFrame({'PRN': prn,'Name':name,'Stream':ug,'Marks':ug_marks})
        writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        # return render(request,'Filter.html',{'data':stu})

    return render(request,'Filter.html',{'data':stu})