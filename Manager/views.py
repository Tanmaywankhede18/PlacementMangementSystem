
from ast import Pass
from weakref import ref
from django.db.models import Q
from contextlib import redirect_stderr
from hashlib import new
from importlib.metadata import requires
from operator import ge
import re
from this import d
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from numpy import deprecate
from openpyxl import Workbook
from pkg_resources import Requirement
from student.models import *
from Manager.models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.contrib.sites.shortcuts import get_current_site  
from django.core.mail import EmailMessage 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from student.token import account_activation_token  
from django.utils.encoding import force_bytes,force_str
from django.core import serializers
import json
from django.core.files.storage import FileSystemStorage
import  pandas as pd 



# Create your views here.


def index(request):
    if(request.method=="POST"):
        print(request.POST)
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
            #Saving the updated Object
            event.save()

            Jresp={
                        'drive_name':event.drive_name,
                        'Desc':event.req,
                        'ctc':event.ctc,
                        'roll':event.roll,
                        'website':event.link,
                        'passout':event.passouts,
                        'lastdate':event.last_date,
                        'id':event.id
            }
                    
            jo = json.dumps(Jresp,default=str)
            return HttpResponse(jo)


            # update event here
            
        elif "update_pass" in request.POST:
            # new_pass = request.POST.get('new_password')
            new_pass = request.POST['update_pass']
            user = request.user
            user.set_password(new_pass)
            user.save()
            login(request,user)
            return HttpResponse("Password Updated Successfully!!")

        elif 'inputData' in request.POST:
            inputData = request.POST['inputData']
            stu = Student.objects.filter(
                Q(PRN__icontains=inputData)|
                Q(first_name__icontains=inputData)|
                Q(email=inputData)|
                Q(mobile=inputData)
            )
            Jresp={}
            for s in stu:
                    Jresp[s.PRN] ={
                        'PRN':s.PRN,
                        'Name':s.first_name,
                        'Email':s.email,
                        'Department':s.ug
                    }
                    
            jo = json.dumps(Jresp,default=str)
            return HttpResponse(jo)

        elif "Action" in request.POST:
            action = request.POST['Action']
            if action != '':
                prn = request.POST['PRN']
                student = Student.objects.get(PRN=prn)
                if action == "Accept":
                    student.verified = 1
                    student.save()
                    HttpResponse("Accepted Request!!")
                elif action == "Reject":
                    student.delete()
                    user = User.objects.get(id=student.user_id)
                    user.delete()
                    print(user)
                    HttpResponse("Rejected Request!!")

                student = Student.objects.filter(verified=0)
                Jresp={}
                for s in student:
                    ug = Student.objects.get(PRN=s.PRN).ug_stream
                    Jresp[s.PRN] ={
                        'PRN':s.PRN,
                        'Name':s.first_name,
                        'Email':s.email,
                        'Department':ug
                    }
                    
                print(Jresp)
                jo = json.dumps(Jresp,default=str)
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
            event = Event(drive_name = name,
            req=Requirement,
            role=roll,
            ctc=ctc,
            passouts = passouts,
            last_date = lastdate,
            link = link
            )
            event.save()
        elif 'updateProfile' in request.POST:
            name=request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            pmObj =PM.objects.get(email=email)
            pmObj.fullname = name
            pmObj.mobile = mobile   
            pmObj.save()
            Jresp={
                        'Mobile':pmObj.mobile,
                        'Name':pmObj.fullname,
                        'Email':pmObj.email,
                        'Department':pmObj.department
            }
                    
            print(Jresp)
            jo = json.dumps(Jresp,default=str)
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
            if id!=None:
                student_list = str(Event.objects.get(id=id).stu_applied) # This will contains the student id's
              
                #Fetch Student name by using their id's 
                
                id_arr = student_list.split(',')
                stu_dic={}
                print("Array of id's:")
                print( id_arr)
                if id_arr[0]!='None':
                    for s_id in id_arr:
                        print(s_id)
                        student_obj = Student.objects.get(user_id=s_id)
                        stu_dic[student_obj.PRN]= student_obj.first_name+" "+student_obj.middle_name+" "+student_obj.last_name

                RequestedEvent = Event.objects.get(id=id)
                Jresp = {
                    'id':RequestedEvent.id,
                    'drive_name':RequestedEvent.drive_name,
                    'Desc':RequestedEvent.req,
                    'roll':RequestedEvent.role,
                    'ctc':RequestedEvent.ctc,
                    'passout':RequestedEvent.passouts,
                    'website':RequestedEvent.link,
                    'lastdate':RequestedEvent.last_date,
                    'students':stu_dic
                }

                jo = json.dumps(Jresp,default=str)
                # print(jo)
                return HttpResponse(jo)
    user = request.user
    events = Event.objects.all()
    st = Student.objects.filter(verified=0)
    if user.is_staff:
        manager = PM.objects.get(email=user.email)
        print(manager)
        return render(request,'PMdashboard.html',{'data':events,'students':st,'Profile':manager})
    try:
        obj = Student.objects.get(user_id=user.id)
    except Student.DoesNotExist:
        return redirect('/Manager/Register')
   
    # Profile = PM.objects.get(user=request.user)
    # print(Profile)
 
    if obj.verified:
        return render(request, 'dashboard.html',{'data':events})
    else:
        return render(request, 'Verfication.html')   




        
def test(request):
    if request.method == 'POST':
            upload = request.FILES['upload']
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            return  render(request,'test.html',{'file':file_url})
            
    stu = Student.objects.all()

    pm=PM.objects.get(email='temp@gmail.com')
    print(pm)



    return render(request,'test.html',{'file':None})



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
            user = User.objects.create_user(email,email,password)
            user.is_staff=True;
            print(name,mobile,dep,email,password)
            user.save()

            pm_obj = PM(
              
                fullname = name,
                email=email,
                mobile=mobile,
                department=dep,
                user = user
            )
            pm_obj.save()

            return HttpResponse("User is created!!")

    return render(request, 'TPORegister.html')

def Login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username!=None:
           user = authenticate(username = username,password = password)

           if user.is_active:
                login(request,user)
                if not user.is_staff:
                    return redirect('/student/Login')
                if user.is_authenticated:
                        return redirect('/Manager/dashboard')
           else:
               return render(request,'Review.html')
               return HttpResponse('Please confirm your email address to complete the registration')    
               
    return render(request,'Login.html')

def Filter(request):
    
    stu = Student.objects.filter()

    if request.method == "POST":
        if "filters" in request.POST:
            name = request.POST['name']
            prn = request.POST['prn']
            # dep = request.POST['dep']
            marks = request.POST['marks']
            gender = request.POST['gender']
            school = request.POST['school']
            gap = request.POST['gap']
            hsc_dep = request.POST['hsc_dep']
            passout = request.POST['passout']
            print(passout)
            search_data = {
            'first_name':name,
            'PRN':prn,
            # 'ug_stream':dep,
            'gender':gender,
            'school_marks':school,
            'ug_passout':passout
            }
            arguments = {}
            for k, v in search_data.items():
                if v:
                    arguments[k] = v
            print(arguments)

            stu = Student.objects.filter(**arguments)

            Jresp ={}
            
            for i in stu:
                Jresp[i.PRN]={
                    'name':i.first_name,
                    'prn':i.PRN,
                    'dep':i.ug_stream,
                    'marks':i.ug_marks
                }
            
          
            jo = json.dumps(Jresp,default=str)
            print(jo)
            return HttpResponse(jo)
        if 'excel' in request.POST:
            getlist = request.POST['list']
            seq_list = json.loads(getlist)
            prn  = []
            name = []
            ug = []
            gender =[]
            ug_marks  = []
            dic = {}
            for s in stu:
                prn.append(s.PRN)
                name.append(str(s.first_name)+" "+str(s.last_name))
                ug.append(s.ug)
                gender.append(s.gender)
                ug_marks.append(s.ug_marks)
            ref_dic= {
                "PRN":prn,
                "Name":name,
                "Marks":ug_marks,
                "UG":ug,
                "Gender":gender
            }
            for x in seq_list:
                dic[x] = ref_dic.get(x)


            df = pd.DataFrame(dic)
            writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.save()

            # print(getlist)
            # file = open('./demo.xlsx', "rb")
            # response = HttpResponse(file.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            # response['Content-Disposition'] = 'attachment; demo.xlsx' 
            # print(response)
            # return response
            # return HttpResponse(getlist)

        name = request.POST.get('name')
        prn = request.POST.get('PRN')
        dep = request.POST.get('Dep')
        marks = request.POST.get('marks')
        skills = request.POST.get('skills')
        gap = request.POST.get('gap')
        gender = request.POST.get('gender')
        school = request.POST.get('school')
        dep_hsc = request.POST.get('12th')
        
        # stu = Student.objects.filter(ug_marks__gte=marks)
        search_data = {
            'first_name':name,
            'PRN':prn,
            'ug_stream':dep,
            'gender':gender,
            'school_marks':school,

        }
        arguments = {}
        for k, v in search_data.items():
            if v:
                arguments[k] = v
        print(arguments)
        stu = Student.objects.filter(**arguments)
        for i in stu:
            print(i.first_name)

        HttpResponse(stu)


       
        # return render(request,'Filter.html',{'data':stu})

    return render(request,'Filter.html')

def ShowProfile(request):
    # if request.method=="GET":
    #     prn = request.GET
    #     stud = Student.objects.get(PRN=prn)
        
    return HttpResponse("Show the User Profile")


  