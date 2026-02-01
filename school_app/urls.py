from django.contrib import admin
from django.urls import path
from school_app import views

urlpatterns = [
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("",views.index),
    path("api", views.getData, name="api"),
    path("index",views.index, name='index'),
    path("about",views.about, name='about'),
    path("contact",views.contact, name='contact'),
    path("admission",views.admission, name='admission'),
    path("admission2",views.admission2, name='enquire'),
    path("reg_submit",views.register),
    path("events",views.EventInfo, name='EventInfo'),
    path("service",views.service, name='service'),
    path("Gallery",views.gallery, name="Gallery"),
    path("mandatory-disclosure",views.MandatoryDisclosure, name="Mandatory-disclosure"),
    # Login/Logout section
    path("login",views.Login, name="login"),
    path("logout",views.Logout, name="logout"),
    # admin section
    path("enquiry",views.enquiry_dashboard, name='enquiry'),
    path("adminDashboard",views.admin, name='adminDashboard'),
    path("enquiry_info/<str:pk>",views.EnquiryInfo, name='Enquiry'),
    path("activities",views.Activities_images, name='Activities'),
    path("events_data",views.Events, name='Events'),
    path("events_data",views.Events, name='Events'),
    path("notices",views.Notices, name='Notice'),
    path("contactinfo",views.Contact_Info, name='ContactInfo'),
    # School gallery
    path("schoolgallery",views.School_gallery, name='School_gallery'),
    path("addInaugration",views.addInaugration, name='addInaugration'),
    path("addAssembly",views.addAssembly, name='addAssembly'),
    path("addFunction",views.addFunction, name='addFunction'),
    path("addPt",views.addPt, name='addPt'),
    # delete section
    path("Delete-Activities/<str:pk>",views.deleteActivity, name='deleteActivities'),
    path("deleteevent/<str:pk>",views.deleteEvent, name='deleteEvent'),
    path("deletenotice/<str:pk>",views.deleteNotice, name='deleteNotice'),
    path("deleteGallery/<str:pk>/<str:pk1>",views.deleteGallery, name='deleteGallery'),
    path("deletecontact/<str:pk>",views.deleteContact, name='deleteContact'),
]
