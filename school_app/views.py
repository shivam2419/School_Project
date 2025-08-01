from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .models import Contact as Cont
import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
import requests
from decouple import config
from time import sleep
BREVO_API_KEY = config('BREVO_API_KEY')

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow:\n"
        "Sitemap: https://www.apsagra.org/sitemap.xml"
    )
    return HttpResponse(content, content_type="text/plain")

@api_view(['GET'])
def getData(request):
    items = registration.objects.all()
    serializer = ItemSerializers(items, many=True)
    return Response(serializer.data)

# Create your views here.
current_time = datetime.datetime.now()
today_date=datetime.date.today()
current_year=current_time.year  

session_context={
    "year":current_year,
    "next_year":current_year+1,
    "over_year":current_year+2,
    "date":today_date
}
# Users section
def index(request):
    if request.method=="POST":
        fname=request.POST.get('f_name')
        lname=request.POST.get('l_name')
        email=request.POST.get('email')
        pnum=request.POST.get('pnum')

        submit=Cont(f_name=fname,l_name=lname,email=email,pnum=pnum)
        submit.save()
        # --- Send Email Confirmation using Brevo ---
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        data_user = {
            "sender": {"name": "Aryabhatt Public School", "email": "csdslt2309@glbitm.ac.in"},
            "to": [{"email": email, "name": fname}],
            "subject": "Contact Form Submitted",
            "htmlContent": f"""
                        <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                            <h2 style="color: #2c3e50;">Admission Query Confirmation – Aryabhatt Public School</h2>
                            <p>Dear <strong>{fname}</strong>,</p>

                            <p>Thank you for contacing with <strong>Aryabhatt Public School</strong>.</p>

                            <p>Our admissions team will contact you shortly for the next steps.</p>

                            <p>If you have any questions, feel free to reach out to us at <a href="mailto:contact@aryabhattpublicschool.com">contact@aryabhattapublicedu@gmail.com</a>.</p>

                            <p>Warm regards,<br>
                            <strong>Aryabhatt Public School</strong><br>
                            Admission Office</p>
                        </body>
                        </html>""",
            "textContent": f"Dear {fname},\nThank you for registering. We have received your admission form."
        }

        requests.post(url, json=data_user, headers=headers)
    stud =event.objects.order_by('-created_at')
    acti=activity.objects.all()
    note=notice.objects.order_by('-created_at')
    s={'stu':stud,'act':acti,'note':note}
    return render(request,('index.html'),s)

def about(request):
    return render(request,('about.html'))

def gallery(request):
    inaug=inaugration.objects.all()
    assem=assembly.objects.all()
    func=function.objects.all()
    pt=Pt.objects.all()
    context={'inaug':inaug,'assem':assem,'func':func,'pt':pt}
    return render(request,('Gallery.html'),context)

def admission(request):
    # todaydate=date.today()
    return render(request,('admission.html'),session_context)

def admission2(request):
    return render(request,('admission2.html'),session_context)

def contact(request):
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pnum=request.POST.get('txt')

        contact_submit=Cont(f_name=fname,l_name=lname,email=email,pnum=pnum)
        contact_submit.save()
    return render(request,('contact.html'))

def service(request):
    return render(request,('service.html'),session_context)

def register(request):
    if request.method == "POST":
        sname = request.POST.get('txtFieldValue_0')
        fname = request.POST.get('txtFieldValue_1')
        mname = request.POST.get('txtFieldValue_2')
        Dob = request.POST.get('txtFieldValue_3')
        pnum = request.POST.get('txtFieldValue_4')
        email = request.POST.get('txtFieldValue_5')
        gender = request.POST.get('txtFieldValue_6')
        applied_for = request.POST.get('txtFieldValue_7')
        last_school = request.POST.get('txtFieldValue_8')
        address = request.POST.get('txtFieldValue_9')
        trans_require = request.POST.get('txtFieldValue_10')

        regis_submit = registration(
            student_name=sname,
            father_name=fname,
            mother_name=mname,
            dob=Dob,
            phone_number=pnum,
            email_id=email,
            gender=gender,
            class_for=applied_for,
            last_schl=last_school,
            address=address,
            trans_req=trans_require
        )
        regis_submit.save()

        # --- Send Email Confirmation using Brevo ---
        url = "https://api.brevo.com/v3/smtp/email"
        
        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }
        # Sending acknowledgement to user
        data_user = {
            "sender": {"name": "Aryabhatt Public School", "email": "csdslt2309@glbitm.ac.in"},
            "to": [{"email": email, "name": sname}],
            "subject": "Admission Form Submitted",
            "htmlContent": f"""
                        <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                            <h2 style="color: #2c3e50;">Admission Query Confirmation – Aryabhatt Public School</h2>
                            <p>Dear <strong>{sname}</strong>,</p>

                            <p>Thank you for registering with <strong>Aryabhatt Public School</strong>. We are pleased to inform you that your admission form has been successfully received.</p>

                            <h3>Submitted Details:</h3>
                            <ul>
                            <li><strong>Student Name:</strong> {sname}</li>
                            <li><strong>Father's Name:</strong> {fname}</li>
                            <li><strong>Mother's Name:</strong> {mname}</li>
                            <li><strong>Date of Birth:</strong> {Dob}</li>
                            <li><strong>Phone Number:</strong> {pnum}</li>
                            <li><strong>Email ID:</strong> {email}</li>
                            <li><strong>Gender:</strong> {gender}</li>
                            <li><strong>Class Applied For:</strong> {applied_for}</li>
                            <li><strong>Previous School:</strong> {last_school}</li>
                            <li><strong>Address:</strong> {address}</li>
                            <li><strong>Transport Required:</strong> {trans_require}</li>
                            </ul>

                            <p>Our admissions team will review your application and contact you shortly for the next steps.</p>

                            <p>If you have any questions, feel free to reach out to us at <a href="mailto:contact@aryabhattpublicschool.com">contact@aryabhattapublicedu@gmail.com</a>.</p>

                            <p>Warm regards,<br>
                            <strong>Aryabhatt Public School</strong><br>
                            Admission Office</p>
                        </body>
                        </html>""",
            "textContent": f"Dear {sname},\nThank you for registering. We have received your admission form."
        }

        requests.post(url, json=data_user, headers=headers)
        
        # Sending data to owner
        data_user = {
            "sender": {
                "name": "Aryabhatt Public School",
                "email": "csdslt2309@glbitm.ac.in"
            },
            "to": [
                {
                    "email": "aryabhattapublicedu@gmail.com",
                    "name": "Aryabhatt Public School"
                }
            ],
            "subject": "New Admission Form Received",
            "htmlContent": f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2 style="color: #2c3e50;">New Admission Form Submitted</h2>
                    <p>Hello Admin,</p>

                    <p>A new admission form has been submitted through the website. Below are the details:</p>

                    <h3>Student Details:</h3>
                    <ul>
                        <li><strong>Student Name:</strong> {sname}</li>
                        <li><strong>Father's Name:</strong> {fname}</li>
                        <li><strong>Mother's Name:</strong> {mname}</li>
                        <li><strong>Date of Birth:</strong> {Dob}</li>
                        <li><strong>Phone Number:</strong> {pnum}</li>
                        <li><strong>Email ID:</strong> {email}</li>
                        <li><strong>Gender:</strong> {gender}</li>
                        <li><strong>Class Applied For:</strong> {applied_for}</li>
                        <li><strong>Previous School:</strong> {last_school}</li>
                        <li><strong>Address:</strong> {address}</li>
                        <li><strong>Transport Required:</strong> {trans_require}</li>
                    </ul>

                    <p>Please check the admin dashboard for full details and next steps.</p>

                    <p>Best regards,<br>
                    <strong>Website Notification System</strong><br>
                    Aryabhatt Public School</p>
                </body>
                </html>
            """,
            "textContent": f"""
        Hello Admin,

        A new admission form has been submitted through the website.

        Student Name: {sname}
        Father's Name: {fname}
        Mother's Name: {mname}
        Date of Birth: {Dob}
        Phone Number: {pnum}
        Email ID: {email}
        Gender: {gender}
        Class Applied For: {applied_for}
        Previous School: {last_school}
        Address: {address}
        Transport Required: {trans_require}

        Please check the admin dashboard for full details.

        Best regards,
        Website Notification System
        Aryabhatt Public School
            """
        }

        requests.post(url, json=data_user, headers=headers)
        return render(request, 'admission.html', {"message": "Registration successful. Confirmation email sent."})

    return render(request, 'admission.html')

def EventInfo(request):
    data = event.objects.all()
    context = {
        'data' : data
    }
    return render(request, 'eventinfo.html', context)


# Login/Logout system
def Login(request):
    if request.method == "POST":
        name = request.POST.get("name")
        pswrd = request.POST.get("password")
        print(name)
        user = authenticate(request, username=name, password=pswrd)
        if user is not None:
            login(request, user)
            return redirect('adminDashboard')  # Redirect to a success page
        else:
            # Return an 'invalid login' error message
            return render(request, 'admin/login.html')

    return render(request, 'admin/login.html')

def Logout(request):
    logout(request)
    return redirect('login')


# Admin section
@login_required(login_url='login')
def admin(request):
    return render(request, 'admin/index.html')

@login_required(login_url='login')
def enquiry_dashboard(request):
    data = registration.objects.all().order_by('-id')
    context = {
        'items' : data
    }
    return render(request, 'admin/dashboard.html', context)

@login_required(login_url='login')
def EnquiryInfo(request, pk):
    try:
        data = registration.objects.get(id=pk)
    except registration.DoesNotExist:
        # Handle the case where the registration with the given id doesn't exist
        return HttpResponse("Data doesn't exists")

    context = {'items': data}
    if request.method == 'POST':
        try:
            Info = registration.objects.get(id=pk)
            Info.delete()
            print('done')
            return redirect('adminDashboard')
        except registration.DoesNotExist:
            # Handle the case where the registration with the given id doesn't exist
            return HttpResponse("Data doesn't exists")

    return render(request, 'admin/enquiry_info.html', context)

@login_required(login_url='login')
def Activities_images(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        files = request.FILES.getlist('file')
        for file in files:
            new_instance = activity(activity=file)
            new_instance.save()
    
    top_obj = activity.objects.order_by('-id').first()
    images = activity.objects.order_by('-created_at')
    if(top_obj):
        top_obj = top_obj.activity.url
        
    context = {
        'images': images,
        'top' : top_obj,
    }
    return render(request, 'admin/activities.html', context)

@login_required(login_url='login')
def deleteActivity(request, pk):
    if request.method == 'POST':
        data = activity.objects.get(id=pk)
        data.delete()
        return redirect('Activities')
    data = activity.objects.get(id=pk)
    return render(request, 'admin/delete_activities.html', {'data' : data})

# Contact section 

@login_required(login_url='login')
def Contact_Info(request):
    contact_info = Cont.objects.all().order_by('-id')
    context = {
        'contact' : contact_info
    }
    return render(request, 'admin/contactinfo.html', context)

@login_required(login_url='login')
def deleteContact(request, pk):
    data = Cont.objects.get(id = pk)
    if request.method == 'POST':
        data.delete()
        return redirect('ContactInfo')
    context = {
        'data' : data
    }
    return render(request, 'admin/deletecontact.html', context)

# Event section

@login_required(login_url='login')
def Events(request):
    if request.method == 'POST':
        name = request.POST.get('event_name')
        desc = request.POST.get('event_desc')

        date_string = request.POST.get('event_date')
        date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        date = date_obj.day
        months_dict = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        month = date_obj.month

        img = request.FILES['event_img']
        print(img)
        obj = event(event = name, event_desc = desc, event_img = img, date = date, month = months_dict[month])
        obj.save()

    data = event.objects.order_by('-created_at')
    context = {
        'data' : data
    }
    return render(request, 'admin/eventsdata.html', context)

@login_required(login_url='login')
def deleteEvent(request, pk):
    if request.method == 'POST':
        data = event.objects.get(id=pk)
        data.delete()
        return redirect('Events')
    data = event.objects.get(id=pk)
    return render(request, 'admin/eventdelete.html', {'data' : data})


# Notice section

@login_required(login_url='login')
def Notices(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        notices = request.POST.get('notice')
        
        obj = notice(date = date, notice = notices)
        obj.save()
    data = notice.objects.order_by('-created_at')
    context = {
        'data' : data
    }
    return render(request, 'admin/noticedata.html', context)

@login_required(login_url='login')
def deleteNotice(request, pk):
    if request.method == 'POST':
        data = notice.objects.get(id=pk)
        data.delete()
        return redirect('Notice')
    data = notice.objects.get(id=pk)
    return render(request, 'admin/deletenotice.html', {'data':data})

# School gallery section

@login_required(login_url='login')
def School_gallery(request):
    return render(request, 'admin/school_gallery.html')


@login_required(login_url='login')
def addInaugration(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        files = request.FILES.getlist('file')
        for file in files:
            new_instance = inaugration(inaugration=file)
            new_instance.save()
    
    top_obj = inaugration.objects.order_by('-id').first()
    images = inaugration.objects.order_by('-created_at')
    if(top_obj):
        top_obj = top_obj.inaugration.url
    own_id = 1
    context = {'top' : top_obj,
               'images' : images,
               'id' : own_id
               }
    return render(request, 'admin/addinaugration.html',context)

@login_required(login_url='login')
def addAssembly(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        files = request.FILES.getlist('file')
        for file in files:
            new_instance = assembly(assembly=file)
            new_instance.save()
    
    top_obj = assembly.objects.order_by('-id').first()
    if top_obj : 
        top_obj = top_obj.assembly.url
    images = assembly.objects.order_by('-created_at')

    own_id = 2
    context = {'top' : top_obj,
               'images' : images,
               'id' : own_id
               }
    return render(request, 'admin/addassembly.html', context)

@login_required(login_url='login')
def addFunction(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        files = request.FILES.getlist('file')
        for file in files:
            new_instance = function(function=file)
            new_instance.save()
    
    top_obj = function.objects.order_by('-id').first()
    if top_obj :
        top_obj = top_obj.function.url
    images = function.objects.order_by('-created_at')

    own_id = 3
    context = {'top' : top_obj,
               'images' : images,
               'id' : own_id
               }
    return render(request, 'admin/addfunction.html', context)

@login_required(login_url='login')
def addPt(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        files = request.FILES.getlist('file')
        for file in files:
            new_instance = Pt(Pt=file)
            new_instance.save()
    
    top_obj = Pt.objects.order_by('-id').first()
    if top_obj :
        top_obj = top_obj.Pt.url
    images = Pt.objects.order_by('-created_at')

    own_id = 4
    context = {'top' : top_obj,
               'images' : images,
               'id' : own_id
               }
    return render(request, 'admin/addpt.html', context)

# Delete from gallery
@login_required(login_url='login')
def deleteGallery(request, pk, pk1):
    if pk == '1':
        obj = inaugration.objects.get(id = pk1)
        obj.delete()
        return redirect('addInaugration')
    elif pk == '2':
        obj = assembly.objects.get(id = pk1)
        obj.delete()
        return redirect('addAssembly')
    elif pk == '3':
        obj = function.objects.get(id = pk1)
        obj.delete()
        return redirect('addFunction')
    elif pk == '4':
        obj = Pt.objects.get(id = pk1)
        obj.delete()
        return redirect('addPt')
    return render(request, 'admin/deletegallery.html')