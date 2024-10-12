from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',home,name='home'),
    path('registration',registration_page,name="registration_page"),
    path('regsave',regsave,name="regsave"),
    path('contact',contact_page,name="contact_page"),
    path('login',login_page,name='login_page'),
    path('logcode',logcode_page,name="logcode_page"),
    path('logout',logout,name='logout'),
    path('studentzone',studentzone,name='studemtzone'),
    path('studenthome',studenthome,name='studenthome'),
    path('updateprofile',updateprofile,name='updateprofile'),
    path('upprofile',upprofile,name='upprofile'),
    path('upsave',upsave,name='upsave'),
    path('adminhome',adminhome,name='adminhome'),
    path('adminlogout',adminlogout,name='adminlogout'),
    path('managestudent/',managestudent,name='managestudent'),
    path('showenq',showenq,name="showenq"),
    path('Usm',Usm,name="Usm"),
    path('Usmsave',Usmsave,name="Usmsave"),
    path('Upload_lecture',Upload_lecture,name="Upload_lecture"),
    path('lecturesave',lecturesave,name="lecturesave"),
    path('viewstudy',viewstudy,name="viewstudy"),
    path('showlecture',showlecture,name='showlecture'),
    path('upload_assignment',upload_assignment,name="upload_assignment"),
    path('uassave',uassave,name="uassave"),
    path('viewAssignment',viewAssignment,name="viewAssignment"),
    path('upload_feedback',upload_feedback,name="upload_feedback"),
    path('feedsave',feedsave,name="feedsave"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
