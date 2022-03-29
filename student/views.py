from django.db import connection, reset_queries
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Manager.models import *
from student.models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.contrib.sites.shortcuts import get_current_site  
from django.core.mail import EmailMessage 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from student.token import account_activation_token  
from django.utils.encoding import force_bytes,force_str


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
                toEmail = email
                email = EmailMessage(  
                                mail_subject, message, to=[email]  
                    )  
                email.send()  
                return render(request,'Email_Verification.html')
                return HttpResponse('Please confirm your email address to complete the registration')  
    
                
                

                

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
            diploma_name = request.POST.get('deploma')
            diploma_marks = request.POST.get('deploma_marks')
            diploma_passout = request.POST.get('deploma_passout')
            diploma_stream = request.POST.get('deploma_stream')
            ssc = request.POST.get('ssc')
            ssc_marks = request.POST.get('ssc_marks')
            ssc_passout  = request.POST.get('ssc_passout')

            stu = Student(
            email = email,
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
            # ug = ug,
            # ug_marks = ug_marks,
            # ug_passout =ug_passout,
            # ug_stream = ug_stream,
            # diploma = deploma,
            # diploma_marks = deploma_marks,
            # diploma_stream = deploma_stream,
            # diploma_passout = deploma_passout,
            # school = ssc,
            # school_marks = ssc_marks,
            # school_passout = ssc_passout,
            user = request.user,
            extra_curriculam = {"Activity 1":'premier legue'}
            )
            stu.save()
            
   
            stud_edu = StudentEducation(
                student =  stu,
                ug_stream = ug,
                ug_passout = ug_passout,
                diploma_college_name = diploma_name,
                diploma_stream = diploma_stream,
                diploma_passout = diploma_passout,
                diploma_total = diploma_marks,
                school_name = ssc,
                school_marks = ssc_marks,
                school_passout = ssc_passout

            )
            stud_edu.save()
            return redirect('/student/dashboard')
        return render(request,'register_div.html')
    else:
        return redirect('/student/Signup')


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
                return redirect('/student/Login')
         
    else:  
        return HttpResponse('Activation link is invalid!')  


def signout(request):
    logout(request)
    return redirect('/Login')

def Signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        if username!=None:
           user = authenticate(username = username,password = password)
           print(user.id)
           stu = Student.objects.get(user_id=user.id)
        #    if user.is_active:

            
           try: 
             print(stu)  
             if stu.verified==1:
                    login(request,user)
                    if not user.is_staff:
                        return redirect('/student/Register')
             else:
                 return render(request,'Review.html')           
           except Student.DoesNotExist:
               return render(request,'Review.html')
               return HttpResponse('Please confirm your email address to complete the registration')    

    else:
        user = request.user
        print(user.id)
        try:
            stu = Student.objects.get(user_id=user.id)
            print('Loggin Your account ')
            login(request,user)
            if not user.is_staff:
                return redirect('/student/dashboard')

        except Student.DoesNotExist:
            print('Register Your account ')
            return redirect('/student/Register')
            return HttpResponse('Please confirm your email address to complete the registration')    


        return redirect('/Login')
   

def index(request):
    user = request.user
    stu = Student.objects.get(user_id=user.id)

    UpdateEducation(request,stu)

    if stu.verified==1:
        events = Event.objects.all()
        ApplyForEvent(request)
        education = StudentEducation.objects.get(student_id=stu.id)
        print(education.diploma_college_name)
        return render(request, 'Student_Dashboard.html',{'data':events,'Education':education,'Personal':stu})
    else:
        print("Inside index")
        return render(request,'Email_verification.html')


def UpdateEducation(request,stu):
    if request.method == "POST":
        if "update_education_specified" in request.POST:
            data_toupdate = json.loads(request.POST['id_arr'])
            print(data_toupdate)
            for i in data_toupdate:
                with connection.cursor() as cursor:
                        cursor.execute('update student_studenteducation  set '+i+'=%s where student_id=%s',[data_toupdate[i],stu.id])
                        
            return HttpResponse("Data Updated Successfully!!")

        if "UpdatePassword" in request.POST:
            if request.method == "POST":
                password = request.POST['id']
                user = request.user
                user.set_password(password)
                user.save()
                login(request,user)
                return HttpResponse("Password Updated Successfully!")    
                
        elif "updateProfile" in request.POST:
            firstName = request.POST.get('Firstname')   
            middleName = request.POST.get('Middlename')
            lastName = request.POST.get('Lastname')
            Email = request.POST.get('Email')
            Birthdate = request.POST.get('Birthdate')
            contact = request.POST.get('Contact')
            address = request.POST.get('Address')
            city = request.POST.get('City')
            state = request.POST.get('State')
            stu.first_name = firstName
            stu.middle_name = middleName
            stu.last_name = lastName
            stu.mobile = contact 
            stu.city = city
            stu.address = address
            stu.state = state
            stu.save()            
            return HttpResponse("Data Updated Successfully!!")

        elif "update_education" in request.POST:
            student_obj = stu
            ug_stream = request.POST.get('ug_stream') 
            ug_admission = request.POST.get('ug_admission')
            ug_passout = request.POST.get('ug_passout')
            ug_fy_sem1 = request.POST.get('ug_fy_sem1')        
            ug_sy_sem1 = request.POST.get('ug_sy_sem1')          
            ug_ty_sem1 = request.POST.get('ug_ty_sem1')          
            ug_be_sem1 = request.POST.get('ug_be_sem1')          
            ug_fy_sem2 = request.POST.get('ug_fy_sem2')          
            ug_sy_sem2 = request.POST.get('ug_sy_sem1')          
            ug_ty_sem2 = request.POST.get('ug_ty_sem1')          
            ug_be_sem2 =request.POST.get('ug_be_sem1')           
            #Atkt
            ug_fy_atkt =request.POST.get('ug_fy_atkt')           
            ug_sy_atkt = request.POST.get('ug_sy_atkt')          
            ug_ty_atkt = request.POST.get('ug_ty_atkt')          
            ug_be_atkt = request.POST.get('ug_be_atkt')          
            #gap
            ug_fy_gap  = request.POST.get('ug_fy_gap')          
            ug_sy_gap  = request.POST.get('ug_sy_gap')         
            ug_ty_gap  = request.POST.get('ug_ty_gap')         
            ug_be_gap  =request.POST.get('ug_be_gap')
            #Diploma
            diploma_college_name =request.POST.get('diploma_college_name')
            diploma_stream =request.POST.get('diploma_stream')            
            diploma_passout = request.POST.get('diploma_passout')  
            diploma_fy = request.POST.get('diploma_fy')          
            diploma_sy = request.POST.get('diploma_sy')          
            diploma_ty = request.POST.get('diploma_ty')          
            diploma_total = request.POST.get('diploma_total')  
            #HSC 
            hsc_college_name = request.POST.get('hsc_college_name')            
            hsc_marks =request.POST.get('hsc_marks')  
            hsc_passout = request.POST.get('hsc_passout')  
            #ssc
            school_name = request.POST.get('school_name')            
            school_marks = request.POST.get('school_marks') 
            school_passout = request.POST.get('school_passout') 

            #Create Object of Student Education
            student_education = StudentEducation(
                student = student_obj,
                ug_stream =ug_stream,
                ug_admission =ug_admission,
                ug_passout =ug_passout,
                ug_fy_sem1 =ug_fy_sem1,
                ug_sy_sem1 =ug_sy_sem1,
                ug_ty_sem1 =ug_ty_sem1,
                ug_be_sem1 =ug_be_sem1,
                ug_fy_sem2 =ug_fy_sem2,
                ug_sy_sem2 =ug_sy_sem2,
                ug_ty_sem2 = ug_ty_sem2,
                ug_be_sem2 =ug_be_sem2,
                #Atkt
                ug_fy_atkt =ug_fy_atkt,
                ug_sy_atkt =ug_sy_atkt,
                ug_ty_atkt =ug_ty_atkt,
                ug_be_atkt =ug_be_atkt,
                #gap
                ug_fy_gap  =ug_fy_gap,
                ug_sy_gap  =ug_sy_gap,
                ug_ty_gap  =ug_ty_gap,
                ug_be_gap  =ug_be_gap,
                #Diploma
                diploma_college_name =diploma_college_name,
                diploma_stream =diploma_stream,
                diploma_passout =diploma_passout,
                diploma_fy =diploma_fy,
                diploma_sy =diploma_sy,
                diploma_ty =diploma_ty,
                diploma_total =diploma_total,
                #HSC 
                hsc_college_name =hsc_college_name,
                hsc_marks =hsc_marks,
                hsc_passout =hsc_passout,
                #ssc
                school_name =school_name,
                school_marks = school_marks,        
                school_passout =school_passout
                )

            print("Update education!!")
        
def ApplyForEvent(request):
    if request.method == "POST":
        if 'apply' in request.POST:
            id = request.POST['id'] # this is id of event 
            event = Event.objects.get(id=id)
            print(event)
            student_list = str(event.stu_applied)
            arr = student_list.split(',')
    
            if arr[0] == 'None':
                student_list=str(request.user.id)
            else:
                student_list+=","+str(request.user.id)
            print(student_list)
            event.stu_applied = student_list
            event.save()

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

    return row