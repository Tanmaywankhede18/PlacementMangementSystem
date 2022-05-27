
from email import message
from errno import ENETDOWN
import io
from multiprocessing import Manager
from posixpath import split
from tkinter import Place
from types import NoneType
from webbrowser import get
from django.db import connection
from django.db.models import Q
from this import d
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import urllib.request
from PlacementManagement import settings
from PlacementManagement.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from student.models import *
from Manager.models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.core.mail import EmailMessage
from django.core import serializers
import json
from django.core.files.storage import FileSystemStorage
import pandas as pd
import boto3
import string
import random
import pdfkit
from django.core.files import File
import shutil
from django.db.models import Value
from django.db.models.functions import Concat


ids = []
ids_dict = {}


def index(request):
    user = request.user
    events = Event.objects.all()
    st = Student.objects.filter(verified=0).filter()
    # Apply Department fileter for this student tables

    if(request.method == "POST"):
        if "update_Event" in request.POST:
            id = request.POST['id']
            name = request.POST['name']
            ctc = request.POST['ctc']
            lastdate = request.POST['lastdate']
            Requirement = request.POST['desc']
            passouts = request.POST['passout']
            link = request.POST['link']
            roll = request.POST['roll']
            event = Event.objects.get(id=id)
            # udpate fields
            event.drive_name = name
            event.last_date = lastdate
            event.ctc = ctc
            event.req = Requirement
            event.passouts = passouts
            event.link = link
            event.role = roll
            # Saving the updated Object
            event.save()

            Jresp = {
                'drive_name': event.drive_name,
                'Desc': event.req,
                'ctc': event.ctc,
                'roll': event.roll,
                'website': event.link,
                'passout': event.passouts,
                'lastdate': event.last_date,
                'id': event.id
            }

            jo = json.dumps(Jresp, default=str)
            return HttpResponse(jo)

        elif "deleteDrive" in request.POST:
            id = request.POST['id']
            Event.objects.get(id=id).delete()
            print(f"Item deleted"+id)

        elif "update_pass" in request.POST:

            new_pass = request.POST['update_pass']
            user = request.user
            user.set_password(new_pass)
            user.save()
            login(request, user)
            return HttpResponse("1")

        elif 'inputData' in request.POST:
            inputData = request.POST['inputData']
            stu = Student.objects.filter(
                Q(PRN__icontains=inputData) |
                Q(first_name__icontains=inputData) |

                Q(email=inputData) |
                Q(mobile=inputData)
            )
            Jresp = {}
            for s in stu:
                Jresp[s.PRN] = {
                    'PRN': s.PRN,
                    'Name': s.first_name+" "+s.middle_name+" "+s.last_name,
                    'Email': s.email,
                    # 'Department':s.ug
                }

            jo = json.dumps(Jresp, default=str)
            return HttpResponse(jo)
        elif 'inputEvent' in request.POST:

            inputData = request.POST['inputEvent']
            filtered_events = Event.objects.filter(
                Q(drive_name__icontains=inputData) |
                Q(role__icontains=inputData) |
                Q(passouts__icontains=inputData) |
                Q(last_date__icontains=inputData)
            )

            Jresp = {}

            for s in filtered_events:
                Jresp[s.pk] = {
                    'drive_name': s.drive_name,
                    'role': s.role,
                    'req': s.req,
                    'passouts': s.passouts,
                    'last_date': s.last_date,
                    'id': s.id
                }
            jo = json.dumps(Jresp, default=str)
            return HttpResponse(jo)

        elif "Action" in request.POST:
            action = request.POST['Action']
            if action != '':
                prn = request.POST['PRN']
                student = Student.objects.get(PRN=prn)
                if action == "Accept":
                    student.verified = 1
                    student.save()
                    # send mail to that specific student
                    mail_subject = "Account Approval"
                    message = "Your account is successfully verified by Department of Technology"
                    email = EmailMessage(
                        mail_subject, message, to=[student.email])
                    email.send()
                    HttpResponse("Accepted Request!!")
                elif action == "Reject":
                    student.delete()
                    user = User.objects.get(id=student.user_id)
                    user.delete()
                    print(user)
                    HttpResponse("Rejected Request!!")

                student = Student.objects.filter(verified=0)
                Jresp = {}
                for s in student:
                    ug = Student.objects.get(PRN=s.PRN).ug_stream
                    Jresp[s.PRN] = {
                        'PRN': s.PRN,
                        'Name': s.first_name,
                        'Email': s.email,
                        'Department': ug
                    }

                print(Jresp)
                jo = json.dumps(Jresp, default=str)
                print(jo)
                return HttpResponse(jo)

        elif "add_event" in request.POST:

            name = request.POST.get("name")
            ctc = request.POST.get("ctc")
            lastdate = request.POST.get("lastdate")
            Requirement = request.POST.get("requirements")
            passouts = request.POST.get("passouts")
            link = request.POST.get("link")
            roll = request.POST.get('roll')
            event = Event(
                drive_name=name,
                req=Requirement,
                role=roll,
                ctc=ctc,
                passouts=passouts,
                last_date=lastdate,
                link=link
            )
            event.save()
            events = Event.objects.all()
            manager = PM.objects.get(email=user.email)
            return render(request, 'PMdashboard.html', {'data': events, 'students': st, 'Profile': manager})

        elif 'updateProfile' in request.POST:
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            pmObj = PM.objects.get(email=email)
            pmObj.fullname = name
            pmObj.mobile = mobile
            pmObj.save()
            Jresp = {
                'Mobile': pmObj.mobile,
                'Name': pmObj.fullname,
                'Email': pmObj.email,
                'Department': pmObj.department
            }

            print(Jresp)
            jo = json.dumps(Jresp, default=str)
            print(jo)
            return HttpResponse(jo)

        elif "updat_profile" in request.POST:
            pm_obj = PM.objects.get(user_id=request.user.id)
            pm_obj.name = request.POST.get('Name')
            pm_obj.mobile = request.POST.get('Mobile')
            pm_obj.dep = request.POST.get('Dep')
            pm_obj.email = request.POST.get('Email')
            pm_obj.save()
        elif "openCard" in request.POST:
            id = request.POST['id']
            if id != None:
                # This will contains the student id's
                student_list = str(Event.objects.get(id=id).stu_applied)

                # Fetch Student name by using their id's

                id_arr = student_list.split(',')
                stu_dic = {}
                print("Array of id's:")
                print(id_arr)
                if id_arr[0] != 'None':
                    for s_id in id_arr:
                        print(s_id)
                        student_obj = Student.objects.get(user_id=s_id)
                        stu_dic[student_obj.PRN] = student_obj.first_name + \
                            " "+student_obj.middle_name+" "+student_obj.last_name

                RequestedEvent = Event.objects.get(id=id)
                Jresp = {
                    'id': RequestedEvent.id,
                    'drive_name': RequestedEvent.drive_name,
                    'Desc': RequestedEvent.req,
                    'roll': RequestedEvent.role,
                    'ctc': RequestedEvent.ctc,
                    'passout': RequestedEvent.passouts,
                    'website': RequestedEvent.link,
                    'lastdate': RequestedEvent.last_date,
                    'students': stu_dic
                }

                jo = json.dumps(Jresp, default=str)
                # print(jo)
                return HttpResponse(jo)

    if user.is_staff:
        manager = PM.objects.get(email=user.email)
        return render(request, 'PMdashboard.html', {'data': events, 'students': st, 'Profile': manager})
    try:
        obj = Student.objects.get(user_id=user.id)
    except Student.DoesNotExist:
        return redirect('/Manager/Register')

    if obj.verified:
        return render(request, 'dashboard.html', {'data': events})
    else:
        return render(request, 'Verfication.html')


def test(request):
    if request.method == 'POST':
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request, 'test.html', {'file': file_url})

    stu = Student.objects.all()

    pm = PM.objects.get(email='temp@gmail.com')
    print(pm)

    return render(request, 'test.html', {'file': None})


def signout(request):
    logout(request)
    return redirect('/Login')


def TPO(request):
    if request.method == "POST":
        if "TPO_register" in request.POST:
            name = request.POST.get('Name')
            mobile = request.POST.get('Mobile')
            dep = request.POST.get('Dep')
            email = request.POST.get('Email')
            password = request.POST.get('Password')
            user = User.objects.create_user(email, email, password)
            user.is_staff = True
            print(name, mobile, dep, email, password)
            user.save()

            pm_obj = PM(

                fullname=name,
                email=email,
                mobile=mobile,
                department=dep,
                user=user
            )
            pm_obj.save()

            return HttpResponse("User is created!!")

    return render(request, 'TPORegister.html')


def Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username != None:
            user = authenticate(username=username, password=password)
            if user is None:
                # show same login page with error
                return render(request, 'Login.html', {'password': True})
                return HttpResponse("Please check your username and password ")
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('/Adw')
                if not user.is_staff:
                    return redirect('/student/Login')
                if user.is_authenticated:
                    return redirect('/Manager/dashboard')
            else:
                return render(request, 'Review.html')

    return render(request, 'Login.html', {'password': False})


def AdminPanel(request):
    checkUser(request)
    if 'deleteTPO' in request.POST:
        user_id = request.POST['id']
        print(request.POST)
        User.objects.get(id=user_id).delete()
        pm = PM.objects.all()
        print("Account Deleted Successfully!")
        return JsonResponse({'error': False, 'message': serializers.serialize('json', pm)})
    elif 'addTpo' in request.POST:

        userName = request.POST['name']
        userMail = request.POST['email']
        dep = request.POST['department']
        mobile = request.POST['mobile']

        if userName and userMail:
            if(User.objects.filter(username=userMail).exists()):
                print("User already exists")
                a = True
            else:
                res = ''.join(random.choices(string.ascii_uppercase +
                                             string.digits, k=8))
                new_user = User.objects.create_user(userMail, userMail, res)
                new_user.is_staff = True
                new_user.save()
                pm = PM(
                    fullname=userName,
                    email=userMail,
                    mobile=mobile,
                    department=dep,
                    user=new_user
                )
                pm.save()

                mail_subject = 'Your account has been created'
                message = "Now your can access your account by user \n Username : " + \
                    userMail+", password : "+res+""
                email = EmailMessage(
                    mail_subject, message, to=[userMail]
                )
                email.send()
                print("User Created Successfully")

    tpo_list = PM.objects.all()
    print(tpo_list)
    return render(request, 'Admin.html', {'list': tpo_list})


def checkUser(req):
    user = req.user
    try:
        obj = User.objects.get(id=user.id)
    except User.DoesNotExist:
        return redirect('/Manager/Register')


def Filter(request):

    stu = Student.objects.filter(verified=1)

    if request.method == "POST":
        NameFormat = ''
        if "deleteStudent" in request.POST:
            student_id = request.POST['student_id']
            Student.objects.get(id=student_id).delete()

        if "filters" in request.POST:
            NameFormat = request.POST['NameFormat']
            return filterdata(request)
        if 'showProfile' in request.POST:
            return redirect('/Manager/Profile')

        if 'excel' in request.POST:
            # NameFormat = request.POST['NameFormat']
            return ExcelUpload(request, NameFormat)

        if 'zip' in request.POST:
            return

    stu = Student.objects.filter(verified=1)

    return render(request, 'Filter.html', {'data': stu})


def ShowProfile(request, prn):
    print(prn)
    # Try and catch student does not exist query
    student = Student.objects.get(PRN=prn)
    student_education = StudentEducation.objects.get(student_id=student.id)
    print(student_education)
    skills = student.extra_curriculam.split(',')
    curri = Cocurriclar.objects.filter(student_id=student.id)
    return render(request, 'Profile.html', {'student': student, 'education': student_education, 'curricular': curri, "skills": skills})


def filterdata(request):
    name = request.POST['name']
    prn = request.POST['prn']

    marks = request.POST['marks']
    marks = marks if marks != '' else 0

    hsc_marks = request.POST['hsc_marks']
    # hsc_marks = 0
    hsc_marks = hsc_marks if hsc_marks != '' else 0

    diploma_marks = request.POST['diploma_marks']
    # diploma_marks = 0
    diploma_marks = diploma_marks if diploma_marks != '' else 0

    gender = request.POST['gender']
    gender = ""+gender[0]+"%" if gender != '' else "%"+"%"

    school = request.POST['school']
    gap = request.POST['gap']
    # hsc_dep = request.POST['hsc_dep']
    passout = request.POST['passout']
    backlog = request.POST['backlogs']
    NameFormat = request.POST['NameFormat']
    Placed = request.POST['Placed']


    multiple_passouts = str(passout).split(',')
    passout_query = 'and ( '
    for i in multiple_passouts:
        temp_q = "student_studenteducation.ug_passout = "+i+" or "
        passout_query = passout_query+temp_q
    passout_query = passout_query[:-3]
    passout_query = passout_query + ")"

    passout_query = passout_query if passout != '' else ""

    backlog = request.POST['backlogs']

    if backlog > '0' and backlog != '':
        backlog = 1

    # use or in name
    # CONCAT_WS(" ",firstname,lastname) = "Sonarika Bhadoria"
    # student_student.first_name like '%"+name+"%' or  student_student.middle_name like '%"+name+"%' or  student_student.last_name like '%"+name+"%'
    #   WHERE CONCAT(TRIM(student_student.first_name), ' ', TRIM(student_student.middle_name),' ',TRIM(student_student.last_name)) LIKE '%"+name+"%'
    #  select * from student_student where CONCAT(TRIM(student_student.first_name), ' ', TRIM(student_student.middle_name),' ',TRIM(student_student.last_name)) LIKE '%Prathmesh Ramesh Sutar%' or student_student.first_name LIKE '%Prathmesh%' or student_student.middle_name LIKE '%Prathmesh%' or student_student.last_name LIKE '%Prathmesh%';
    # select * from student_student where CONCAT(TRIM(student_student.first_name), ' ', TRIM(student_student.middle_name),' ',TRIM(student_student.last_name)) LIKE '%"+name+"%' or student_student.first_name LIKE '%"+name+"%' or student_student.middle_name LIKE '%"+name+"%' or student_student.last_name LIKE '%"+name+"%';

    q = "select student_student.first_name,student_student.middle_name,student_student.last_name, student_student.PRN,student_student.gender,student_student.birth_date, student_studenteducation.ug_passout,student_studenteducation.school_marks, student_student.id, student_studenteducation.id from student_studenteducation join student_student on student_student.id = student_studenteducation.student_id where ( CONCAT(TRIM(student_student.first_name), ' ', TRIM(student_student.middle_name),' ',TRIM(student_student.last_name)) LIKE '%"+name+"%' or student_student.first_name LIKE '%"+name+"%' or student_student.middle_name LIKE '%"+name+"%' or student_student.last_name LIKE '%"+name+"%') and student_student.PRN like '%"+str(
        prn)+"%' and student_studenteducation.school_marks > '"+str(school)+"'  and student_student.gender like '"+gender+"' and student_studenteducation.ug_total > '"+str(marks)+"' and student_studenteducation.ug_backlog = '"+str(backlog)+"'  and student_studenteducation.hsc_marks > '"+str(hsc_marks)+"' and student_studenteducation.diploma_total > '"+str(diploma_marks)+"' and student_studenteducation.gap = "+gap+" and student_student.verified > 0  " + str(passout_query)+" "

    print(q)
    cursor = connection.cursor()
    cursor.execute(q)
    result = cursor.fetchall()
    print(NameFormat)
    jobj = arraytojson(result, NameFormat)
    # for  i in ids_dict:
    #     get_student = Student.objects.get(id=i)
    #     get_education = StudentEducation.objects.get(id=ids_dict[i])

    return JsonResponse({'error': False, 'message': jobj})


def arraytojson(tu, NameFormat):
    # ids_dict = {}
    jsres = {}
    print(NameFormat)
    for arr in tu:
        ids.append(arr[3])
        ids_dict[arr[8]] = arr[9]
        print(NameFormat)
        if NameFormat == "fms":
            Name = str(arr[0])+" "+str(arr[1])+" "+str(arr[2])
        else:
            Name = str(arr[2])+" "+str(arr[0])+" "+str(arr[1])
        try:
            resume_url = Student.objects.get(id=arr[8]).resume.url
        except ValueError:
            resume_url = ""
        print(resume_url)
        json_data = {
            'name': Name,
            'prn': arr[3],
            'gender': arr[4],
            'url': resume_url,
            'marks': StudentEducation.objects.get(id=arr[9]).ug_total

        }
        jsres[arr[3]] = json_data
    return jsres


def ExporttoExcel(NameFormat):
    arr_ids = ids_dict
    print(arr_ids)
    excel_dict = {
        "Name": [],
        "PRN": [],
        "Gender": [],
        "BTech": [],
        "Passout": [],
        "Backlog": [],
        "Deploma": [],
        "HSC": [],
        "SSC": [],
        "BirthDate": [],
        "Email": [],
        'Mobile': [],
        "Address": [],
        "ResumeURL": []
    }
    for i in arr_ids:

        get_student = Student.objects.get(id=i)
        get_education = StudentEducation.objects.get(id=arr_ids[i])

        Name = get_student.first_name+" "+get_student.middle_name+" "+get_student.last_name

        if NameFormat == 'fms':
            Name = get_student.first_name+" "+get_student.middle_name+" "+get_student.last_name
        else:
            Name = get_student.last_name+" "+get_student.first_name+" "+get_student.middle_name

        excel_dict['Name'].append(Name)
        excel_dict['PRN'].append(get_student.PRN)
        excel_dict['Gender'].append(get_student.gender)
        excel_dict['BTech'].append(get_education.ug_total)
        excel_dict['Passout'].append(get_education.ug_passout)
        excel_dict['Deploma'].append(get_education.diploma_total)
        excel_dict['Backlog'].append(get_education.ug_backlog)
        excel_dict['HSC'].append(get_education.hsc_marks)
        excel_dict['SSC'].append(get_education.school_marks)
        excel_dict['BirthDate'].append(str(get_student.birth_date))
        excel_dict['Email'].append(str(get_student.email))
        excel_dict['Address'].append(str(get_student.address))
        excel_dict['Mobile'].append(str(get_student.mobile))
        resume_url_temp = str(get_student.resume.url) if (
            get_student.resume.url) else ""
        excel_dict['ResumeURL'].append(resume_url_temp)
    return excel_dict


def ExcelUpload(request, NameFormat):
    print(NameFormat)
    ref_dic = ExporttoExcel(NameFormat)
    user = request.user
    pm_obj = PM.objects.get(user_id=user.id)
    isExist = os.path.exists(settings.MEDIA_ROOT+"/PDF/"+pm_obj.department)
    if not isExist:
        isExist = os.makedirs(settings.MEDIA_ROOT+"/PDF/"+pm_obj.department)
    if "zip" in request.POST:
        for i in ref_dic['ResumeURL']:
            index_slash = i.rfind('/')
            index_dot = i.rfind('.')
            pdf_name = i[index_slash:index_dot]
            download_file(i, pdf_name, pm_obj)
        shutil.make_archive(settings.MEDIA_ROOT+"/"+pm_obj.department,
                            'zip', settings.MEDIA_ROOT+"/PDF/"+pm_obj.department)
        return JsonResponse({"error": False, "message": "/media/"+pm_obj.department+".zip"})

    getlist = request.POST['list']
    # You dont need this line because we have already loaded getlist with array
    seq_list = json.loads(getlist)
    dic = {}
    if seq_list == None:
        print("List is empty !!!")
    for x in seq_list:
        dic[x] = ref_dic.get(x)

    df = pd.DataFrame(dic)
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    c = output.getvalue()
    bucket = 'placementmanagement'
    region = 'ap-south-1'
    file_name = pm_obj.department+'.xlsx'
    s3 = boto3.resource('s3', aws_access_key_id="AKIA6BYQTIORN7JWRPWI",
                        aws_secret_access_key="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")
    d = s3.Bucket(bucket).put_object(Key=file_name, Body=c)

    url = f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}"
    if "pdfofexcel" in request.POST:
        df = pd.read_excel(url)

        df.to_html(settings.MEDIA_ROOT+"/"+pm_obj.department+".html")
        pdfkit.from_file(settings.MEDIA_ROOT+"/"+pm_obj.department +
                         ".html", settings.MEDIA_ROOT+"/"+pm_obj.department+".pdf")

    return JsonResponse({'error': False, 'message': url})


def download_file(download_url, filename, pm_obj):
    response = urllib.request.urlopen(download_url)
    file = open(settings.MEDIA_ROOT+"/PDF/" +
                pm_obj.department+"/" + filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()


def PlacedFilter(request):
    Placed_students = Student.objects.all()
    students = []
    for i in Placed_students:
        Placement = Placementinfo.objects.filter(student_id=i.id)
        students.append({
            "student_data": i,
            "company_data": Placement

        })

    if request.method == "POST":
        user = request.user
        get_current_tpo = PM.objects.get(user_id = user.id)

        name = request.POST['req_data']
        # filterd_students = Student.objects.filter(
        #     Q(first_name__icontains=name) |
        #     Q(middle_name__icontains=name) |
        #     Q(last_name__icontains=name))
        print(name)
        filterd_students = Student.objects.annotate(full_name = Concat('first_name',Value(' '),'last_name'))

        query =  "select concat(student_student.first_name,' ',student_student.middle_name,' ',student_student.last_name), student_student.PRN , student_student.id  from student_student  where (( CONCAT(TRIM(student_student.first_name), ' ', TRIM(student_student.middle_name),' ',TRIM(student_student.last_name)) LIKE '%"+name+"%' or student_student.first_name LIKE '%"+name+"%' or student_student.middle_name LIKE '%"+name+"%' or student_student.last_name LIKE '%"+name+"%')) and student_student.PlacementStatus = 1 and student_student.Department LIKE '%"+get_current_tpo.department+"%'"
        
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # Result will contains only one element at 0 th position 
        # this result will contains array of data 
        student_id_arr = []
        for i in result:
            student_id_arr.append(i)
        
        company_details = {}
        for i in student_id_arr:
            # i have at 0 th index full name 1 index prn 2 index there will be an id 
            # THis is working code 
            get_companies = Placementinfo.objects.filter(student_id=i[2])
            if get_companies.count() == 0:
                continue

            temp_obj = {}
            count = 0;
            for j in get_companies:
                temp_obj[count]={
                    "Name":j.CompanyName,
                    "url":j.Offerletter.url,
                }
                count=count+1
            company_details[i[2]] = {
                'Name': i[0],
                'Company':temp_obj,
                "PRN":i[1]
            }
        return JsonResponse({"error": False, "message": company_details})
    return render(request, 'PlacedFilter.html', {'placedstudents': students})
