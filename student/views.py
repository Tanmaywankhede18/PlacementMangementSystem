from tkinter import Place
from unittest import result
from django.db import connection, reset_queries
import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from Manager.models import *
import student
from student.forms import ImageUpload, OfferLetterUpload, ResumeUpload
from student.models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from student.token import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.core import serializers

def signup(request):
    email = request.POST.get('Email')
    a = False
    if email != None:
        if(User.objects.filter(username=email).exists()):
            print("User already exists")
            a = True
        else:
            Password = request.POST.get('Pass')
            new_user = User.objects.create_user(email, email, Password)
            new_user.save()
            current_site = get_current_site(request)
            print(current_site)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            toEmail = email
            email = EmailMessage(
                mail_subject, message, to=[email]
            )
            email.send()
            return render(request, 'Email_Verification.html')
            return HttpResponse('Please confirm your email address to complete the registration')

    return render(request, 'Signup.html', {'message_exist': a})


def register(request):
    if request.user.is_authenticated:
        if Student.objects.filter(user_id=request.user.id):
            print("User Filled his form")

        if request.method == 'POST':
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
            ug_backlogs = request.POST.get('current_backlog')
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
            ssc_passout = request.POST.get('ssc_passout')
            gap = request.POST.get('Gap')

            # 12 Th data collection 
            hsc = request.POST.get('hsc') 
            hsc_marks = request.POST.get('ssc_marks')
            hsc_passout = request.POST.get('ssc_passout')
            

            stu = Student(
                email=email,
                verified=False,
                first_name=firstname,
                middle_name=middlename,
                last_name=lastname,
                birth_date=birth_date,
                gender=gender,
                address=address,
                city=city,
                state=state,
                mobile=mobile,
                PRN=prn,
                user=request.user,
                extra_curriculam={},
                Department = ug_stream
            )
            stu.save()

            stud_edu = StudentEducation(
                student=stu,
                # ug = "Department of Technology",
                ug_stream = ug_stream,
                ug_total = ug_marks,
                ug_passout=ug_passout,
                diploma_college_name=diploma_name,
                diploma_stream=diploma_stream,
                diploma_passout=diploma_passout,
                diploma_total=diploma_marks,
                school_name=ssc,
                school_marks=ssc_marks,
                school_passout=ssc_passout,
                gap=gap,
                hsc_college_name = hsc,
                hsc_marks = hsc_marks,
                hsc_passout = hsc_passout
            )
            stud_edu.save()
            return redirect('/student/dashboard')
        return render(request, 'register_div.html')
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
        login(request, user)
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

        if username != None:
            user = authenticate(username=username, password=password)
            stu = Student.objects.get(user_id=user.id)
        #    if user.is_active:
            try:
                if stu.verified == 1:
                    login(request, user)
                    if not user.is_staff:
                        return redirect('/student/Register')
                else:
                    return render(request, 'Review.html')
            except Student.DoesNotExist:
                return render(request, 'Review.html')

    else:
        user = request.user
        print(user.id)
        try:
            stu = Student.objects.get(user_id=user.id)
            print('Loggin Your account ')
            login(request, user)
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
    UpdateEducation(request, stu)
    DeleteResume(request)

    if "search_event" in request.POST:
        input_Data  = request.POST.get('search_event')
        event_array = Event.objects.filter(
            Q(drive_name__icontains = input_Data)|
            Q(role__icontains = input_Data)|
            Q(req__icontains = input_Data)|
            Q(ctc__icontains = input_Data)|
                Q(passouts__icontains = input_Data)
        )
        qs_json = serializers.serialize('json', event_array)
        # return HttpResponse(qs_json, content_type='application/json')
        return JsonResponse({'error':False,'message':qs_json})

    if stu.verified == 1:
        events = Event.objects.all()
        if 'apply' in request.POST:
            return ApplyForEvent(request)
        form = ImageUpload()
        r_form = ResumeUpload()
        offer_letter = OfferLetterUpload()

        education = StudentEducation.objects.get(student_id=stu.id)
        placed = Placementinfo.objects.filter(student_id=stu.id)

        # try:
        #     plc_id = stu.placementref_id
        # except Placementinfo.DoesNotExist:
        #     Placement = Placementinfo.objects.get(id=plc_id)

        Placement = None
        if request.method == 'POST':
            if "DeleteC" in request.POST:
                id = request.POST['id']
                cu = Cocurriclar.objects.get(id=id)
                cu.delete()
                cu = Cocurriclar.objects.all()
                JSON_Response = {}
                JSON_Object_Curricular = {}
                for q in cu :
                    JSON_Object_Curricular['Name'] = q.CompanyName
                    JSON_Object_Curricular['Description'] = q.Description
                    JSON_Response[q.id] = JSON_Object_Curricular
                    JSON_Object_Curricular = {}
                return JsonResponse({'error':False,'message': JSON_Response})

            if "UpdateC" in request.POST:
                id = request.POST['id']
                Company_Name = request.POST['Name']
                Desc = request.POST['Desc']
                cu = Cocurriclar.objects.get(id=id)
                cu.CompanyName = Company_Name
                cu.Description = Desc
                cu.save()
                cu = Cocurriclar.objects.all()
                JSON_Response = {}
                JSON_Object_Curricular = {}
                for q in cu :
                    JSON_Object_Curricular['Name'] = q.CompanyName
                    JSON_Object_Curricular['Description'] = q.Description
                    JSON_Response[q.id] = JSON_Object_Curricular
                    JSON_Object_Curricular = {}
                return JsonResponse({'error':False,'message': JSON_Response})

            if "AddCo" in request.POST:
            
                company_name = request.POST['name']
                description = request.POST['description']
                co = Cocurriclar(
                    CompanyName=company_name,
                    Description=description,
                    student = stu
                )
                co.save()
                curricular = Cocurriclar.objects.filter(student_id=stu.id)
                JSON_Response = {}
                JSON_Object_Curricular = {}
                for q in curricular :
                    JSON_Object_Curricular['Name'] = q.CompanyName
                    JSON_Object_Curricular['Description'] = q.Description
                    JSON_Response[q.id] = JSON_Object_Curricular
                    JSON_Object_Curricular = {}

                print(JSON_Response)
                return JsonResponse({'error':False,'message':JSON_Response})


            if "HRname" in request.POST:
                offer_letter = OfferLetterUpload(request.POST,request.FILES)
             
                if offer_letter.is_valid:
                    # offer_letter.student_id = stu.id
                    c = offer_letter.save()
                    c.student_id = stu.id
                    c.save()
                    get_current_student = Student.objects.get(id = stu.id)
                    get_current_student.PlacementStatus = True
                    get_current_student.save()
                    
                    company_json = {}
                    offere_letter_array = Placementinfo.objects.filter(student_id = stu.id)
                    print("Printing array of offere letters ")
                    for i in offere_letter_array:
                        company_json[i.id] = {
                            "Name" : i.CompanyName,
                            "CTC" : i.CTC,
                            "JoinDate": i.JoinDate,
                            "Role" : i.Role,
                            "OfferLetter": i.Offerletter.url
                        }


                    return JsonResponse({'error':False,'message':company_json})
                    # stu.placementref_id = c.id
                    # stu.save()
                    # p = Placementinfo.objects.get(id=stu.placementref_id)
                    # print(p.Offerletter.url)


            elif "uploadProfile" in request.POST:
                form = ImageUpload(request.POST, request.FILES)
                stu.profile = request.FILES['profile']
                stu.save()
                JsonResponse({'error': False, 'message': stu.profile.url})
                return JsonResponse({'error': False, 'message': stu.profile.url})
                
            elif 'resume' in request.FILES:
                r_form = ResumeUpload(request.POST,request.FILES)
                stu.resume = request.FILES['resume']
                stu.save()
                return JsonResponse({'error':False,'message':stu.resume.url})

        cocur = Cocurriclar.objects.filter(student_id = stu.id)      

        context = {
            'data': events, 
            'Education': education, 
            'Personal': stu, 
            'Plcement': Placement, 
            'form': form,
            'resume_form':r_form,
            'offer_letter':offer_letter,
            'Placed':placed,
            'curricular':cocur
            }
        return render(request, 'Student_Dashboard.html',context)
    else:
        return render(request, 'Email_verification.html')




def UpdateEducation(request, stu):
    if request.method == "POST":
        if "update_education_specified" in request.POST:
            data_toupdate = json.loads(request.POST['id_arr'])
            print(data_toupdate)
            for i in data_toupdate:
                with connection.cursor() as cursor:
                    cursor.execute('update student_studenteducation  set ' +
                                   i+'=%s where student_id=%s', [data_toupdate[i], stu.id])

            return HttpResponse("Data Updated Successfully!!")
     
    
        if "UpdatePassword" in request.POST:
            if request.method == "POST":
                password = request.POST['id']
                user = request.user
                user.set_password(password)
                user.save()
                login(request, user)
                return HttpResponse("Password Updated Successfully!")
            return JsonResponse({'error': False})
        elif "updatEx" in request.POST:
            data = request.POST
            stu.extra_curriculam = data['exData']
            stu.save()
            return HttpResponse("Password Updated Successfully!")

        elif "updateProfile" in request.POST:
            firstName = request.POST.get('Firstname')
            middleName = request.POST.get('Middlename')
            lastName = request.POST.get('Lastname')
            Email = request.POST.get('Email')
            Birthdate = request.POST.get('Birthdate')
            print(Birthdate,stu.birth_date)
            Birthdate = stu.birth_date if Birthdate == '' else Birthdate
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
            stu.birth_date = Birthdate
            stu.save()
            return JsonResponse({'error': False})

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
            ug_be_sem2 = request.POST.get('ug_be_sem1')
            # Atkt
            ug_fy_atkt = request.POST.get('ug_fy_atkt')
            ug_sy_atkt = request.POST.get('ug_sy_atkt')
            ug_ty_atkt = request.POST.get('ug_ty_atkt')
            ug_be_atkt = request.POST.get('ug_be_atkt')
            # gap
            ug_fy_gap = request.POST.get('ug_fy_gap')
            ug_sy_gap = request.POST.get('ug_sy_gap')
            ug_ty_gap = request.POST.get('ug_ty_gap')
            ug_be_gap = request.POST.get('ug_be_gap')
            # Diploma
            diploma_college_name = request.POST.get('diploma_college_name')
            diploma_stream = request.POST.get('diploma_stream')
            diploma_passout = request.POST.get('diploma_passout')
            diploma_fy = request.POST.get('diploma_fy')
            diploma_sy = request.POST.get('diploma_sy')
            diploma_ty = request.POST.get('diploma_ty')
            diploma_total = request.POST.get('diploma_total')
            # HSC
            hsc_college_name = request.POST.get('hsc_college_name')
            hsc_marks = request.POST.get('hsc_marks')
            hsc_passout = request.POST.get('hsc_passout')
            # ssc
            school_name = request.POST.get('school_name')
            school_marks = request.POST.get('school_marks')
            school_passout = request.POST.get('school_passout')

            # Create Object of Student Education
            student_education = StudentEducation(
                student=student_obj,
                ug_stream=ug_stream,
                ug_admission=ug_admission,
                ug_passout=ug_passout,
                ug_fy_sem1=ug_fy_sem1,
                ug_sy_sem1=ug_sy_sem1,
                ug_ty_sem1=ug_ty_sem1,
                ug_be_sem1=ug_be_sem1,
                ug_fy_sem2=ug_fy_sem2,
                ug_sy_sem2=ug_sy_sem2,
                ug_ty_sem2=ug_ty_sem2,
                ug_be_sem2=ug_be_sem2,
                # Atkt
                ug_fy_atkt=ug_fy_atkt,
                ug_sy_atkt=ug_sy_atkt,
                ug_ty_atkt=ug_ty_atkt,
                ug_be_atkt=ug_be_atkt,
                # gap
                ug_fy_gap=ug_fy_gap,
                ug_sy_gap=ug_sy_gap,
                ug_ty_gap=ug_ty_gap,
                ug_be_gap=ug_be_gap,
                # Diploma
                diploma_college_name=diploma_college_name,
                diploma_stream=diploma_stream,
                diploma_passout=diploma_passout,
                diploma_fy=diploma_fy,
                diploma_sy=diploma_sy,
                diploma_ty=diploma_ty,
                diploma_total=diploma_total,
                # HSC
                hsc_college_name=hsc_college_name,
                hsc_marks=hsc_marks,
                hsc_passout=hsc_passout,
                # ssc
                school_name=school_name,
                school_marks=school_marks,
                school_passout=school_passout
            )
            student_education.save()
            return JsonResponse({'error': False})


def ApplyForEvent(request):
    if request.method == "POST":
        if 'apply' in request.POST:
            id = request.POST['id']  # this is id of event
            event = Event.objects.get(id=id)
            student_list = str(event.stu_applied)
            arr = student_list.split(',')

            if arr[0] == 'None':
                student_list = str(request.user.id)
            else:
                student_list += ","+str(request.user.id)
            event.stu_applied = student_list
            event.save()
        return JsonResponse({'error': False,'message':event.link})

def DeleteResume(request):
    if request.method == 'POST':
        if "deleteResume" in request.POST:
            print(request.POST['id'])
            stu_id = request.POST['id']
            student_obj = Student.objects.get(id=stu_id)
            print(student_obj.first_name)
            student_obj.resume.delete(save=True)
            print('Resume Deleted ')

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()

    return row
