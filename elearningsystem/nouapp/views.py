from django.shortcuts import render,HttpResponse,redirect
from django.utils import timezone
from .models import login, registration, tbl_contact,tbl_Usm,upload_lecture,upload_assign,Feedback,Complaints
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.core.mail import send_mail
from .import smssender

# Create your views here.
def home(request):
    return render(request,'home.html')

def registration_page(request):
    return render(request,'registration.html')

def regsave(request):
    rollno=request.POST['rollno']
    name=request.POST['name']
    fname=request.POST['fname']
    mname=request.POST['mname']
    gender=request.POST['gender']
    address=request.POST['address']
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    contactno=request.POST['contactno']
    email=request.POST['email']
    password=request.POST['password']
    regdate=timezone.now()
    usertype='student'
    status='pending'
    ab=registration(rollno=rollno,name=name,fname=fname,mname=mname,gender=gender,address=address,program=program,branch=branch,year=year,contactno=contactno,email=email,password=password,regdate=regdate)
    bc=login(userId=email,password=password,usertype=usertype,status=status)
    ab.save()
    bc.save()
    # Prepare email content
    subject = 'Registration Confirmation'
    message = f'''
    Welcome to Nou Egyan!
    We’re excited to have you as a part of our community. 
    Below, you’ll find your login details for accessing the Nou Egyan portal.

    Your Userid And Password is:
    Userid: {email}
    Password: {password}

    Please keep this information secure and do not share it with anyone.
    '''
    from_email = 'ramest2115443@akgec.ac.in'
    recipient_list = [email]

        # Send email
    send_mail(subject, message, from_email, recipient_list)

        # Add success message and redirect
    messages.success(request, 'Registration successful! Please check your email for confirmation.')
    return render(request, 'registration.html') # Replace with your success URL
      #  return redirect('registartion')
    # return redirect('registration_page')

def contact_page(request):
    if request.method=='POST':
        name=request.POST['name']
        gender=request.POST['gender']
        address=request.POST['address']
        contactno=request.POST['contactno']
        email=request.POST['email']
        enquirytext=request.POST['enquirytext']
        enqdate=timezone.now()
        cs=tbl_contact(name=name,gender=gender,address=address,contactno=contactno,email=email,enquirytext=enquirytext,enqdate=enqdate)
        cs.save()
        smssender.sendsms(contactno)
        return redirect('home')
    return render(request,'contactus.html')

def login_page(request):
    return render(request,'login.html')

def logcode_page(request):
    if request.method=="POST":
        userId=request.POST['userId']
        password=request.POST['password']
        usertype=request.POST['usertype']
        user=login.objects.filter(userId=userId,password=password).first()
        if user:
            if user.usertype=="student" and usertype=="student":
                request.session['userId']=userId
                return redirect('studenthome')
            elif user.usertype=="admin" and usertype=="admin":
                return redirect('adminhome')
            else:
                return redirect('login_page')
        else:
            return redirect('login_page')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def studentzone(request):
    if 'userId' in request.session:
        return redirect('studenthome')
    else:
        return redirect('login_page')
    

def logout(request):
    request.session.flush()
    return redirect('login_page')

def studenthome(request):
    return render(request,'studenthome.html')

def updateprofile(request):
    user_email=request.session.get('userId')
    user=registration.objects.filter(email=user_email).first()
    show={
        'show':user
    }
    return render(request,'updateprofile.html',show)

def upprofile(request):
    user_email=request.session.get('userId')
    user=registration.objects.filter(email=user_email).first()
    # user data
    show={
        'show':user
    }
    return render(request,'upprofile.html',show)

def upsave(request):
    user_email=request.session.get('userId')
    user=registration.objects.filter(email=user_email).first()
    if user:
        user.rollno=request.POST['rollno']
        user.name=request.POST['name']
        user.fname=request.POST['fname']
        user.mname=request.POST['mname']
        user.gender=request.POST['gender']
        user.address=request.POST['address']
        user.program=request.POST['program']
        user.branch=request.POST['branch']
        user.year=request.POST['year']
        user.contactno=request.POST['contactno']
        user.email=request.POST['email']
        user.password=request.POST['password']
        if 'profile_pic' in request.FILES:
            user.profile_pic=request.FILES['profile_pic']
        user.save()
        return redirect('updateprofile')
    
def adminzone(request):
    return render(request,'adminzone.html')

def adminhome(request):
    return render(request,'adminhome.html')

def adminlogout(request):
    request.session.flush()
    return redirect('login_page')

def managestudent(request):
    ab=registration.objects.all()
    return render(request,'managestudent.html',{'show':ab})
        
def showenq(request):
    ab=tbl_contact.objects.all()
    return render(request,'showenq.html',{'show':ab})

def Usm(request):
    ab=tbl_Usm.objects.all()
    return render(request,'Usm.html',{'ab':ab})

def Usmsave(request):
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    new_file=request.FILES['new_file']
    av=tbl_Usm(program=program,branch=branch,year=year,subject=subject,new_file=new_file)
    av.save()
    messages.success(request,'Study Material Upload Successfully')
    return redirect('Usm')

def Upload_lecture(request):
    ab=upload_lecture.objects.all()
    return render(request,'upload_lecture.html',{'ab':ab})

def lecturesave(request):
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    link=request.POST['link']
    av=upload_lecture(program=program,branch=branch,year=year,subject=subject,link=link)
    av.save()
    messages.success(request,'Lecture Uploaded Successfully!!!')
    return render(request,'upload_lecture.html')

def viewstudy(request):
    if 'userId' in request.session:
        # branch=request.session.get('branch')
        # if branch:
        #     ab=tbl_Usm.object.filter(branch=branch).first()
        #     return render(request,'viewstudy.html',{'ab':ab})
        # else:
        #     messages.error(request,'Branch Information is missing')
        ab=tbl_Usm.objects.all()
        return render(request,'viewstudy.html',{'ab':ab})
    else:
        return redirect('login_page')
    
def showlecture(request):
    if 'userId' in request.session:
        ab=upload_lecture.objects.all()
        return render(request,'viewlecture.html',{'ab':ab})
    else:
        return redirect('login_page')
    
def upload_assignment(request):
    ab=upload_assign.objects.all()
    return render(request,'upload_assignment.html',{'ab':ab})
    
def uassave(request):
    program=request.POST['program']
    branch=request.POST['branch']
    year=request.POST['year']
    subject=request.POST['subject']
    new_file=request.FILES['new_file']
    av=upload_assign(program=program,branch=branch,year=year,subject=subject,new_file=new_file)
    av.save()
    messages.success(request,'Assignment Upload Successfully')
    return redirect('upload_assignment')

def viewAssignment(request):
    if "userId" in request.session:
        ab=upload_assign.objects.all()
        return render(request,'viewAssignment.html',{'ab':ab})
    else:
        return redirect("login_page")
    
def upload_feedback(request):
    ab=Feedback.objects.all()
    return render(request,'feedback.html',{'ab':ab})

def feedsave(request):
    if request.method=='POST':
        subject=request.POST.get('subject')
        feedback=request.POST.get('feed')
        user_email=request.session.get('userId')
        user=registration.objects.filter(email=user_email).first()
        if user:
            Feedback.objects.create(
                name=user.name,
                program=user.program,
                branch=user.branch,
                year=user.year,
                subject=subject,
                feed=feedback,
                reqdate=timezone.now()
            )
            messages.success(request,'Feedback Submitted Successfully!!')
        else:
            messages.success(request,'Not Found')
        return render(request,'feedback.html')
    return redirect('upload_feedback')
    
def upload_comp(request):
    ab=Complaints.objects.all()
    return render(request,'complaint.html',{'ab':ab})

def compsave(request):
    if request.method=='POST':
        subject=request.POST.get('subject')
        comp=request.POST.get('comp')
        user_email=request.session.get('userId')
        user=registration.objects.filter(email=user_email).first()
        if user:
            Complaints.objects.create(
                name=user.name,
                program=user.program,
                branch=user.branch,
                year=user.year,
                subject=subject,
                comp=comp,
                reqdate=timezone.now()
            )
            messages.success(request,'Complaint Submitted Successfully!!')
        else:
            messages.success(request,'Not Found')
        return render(request,'complaint.html')
    return redirect('upload_comp')

def deletefeed(request,id):
    ab=Feedback.objects.get(pk=id)
    ab.delete()
    return redirect('upload_feedback')

def deletecomp(request,id):
    ab=Complaints.objects.get(pk=id)
    ab.delete()
    return redirect('upload_comp')

def viewcomp(request):
    show=Complaints.objects.all()
    return render(request,'viewcomp.html',{'show':show})

def viewfeed(request):
    show=Feedback.objects.all()
    return render(request,'viewfeed.html',{'show':show})

def deleteAdmincomp(request,id):
    ab=Complaints.objects.get(pk=id)
    ab.delete()
    return render(request,'viewcomp.html')

def deleteAdminfeed(request,id):
    ab=Feedback.objects.get(pk=id)
    ab.delete()
    return render(request,'viewfeed.html')
