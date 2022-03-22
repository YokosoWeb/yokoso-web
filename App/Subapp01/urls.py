
from django.contrib import admin
from django.urls import path, include, re_path
from .views import *
from Subapp01 import views


urlpatterns = [
    path('', home , name = 'home'),
    path('signin/', signin , name = 'signin'),
    path('signup/', signup , name = 'signup'),
    path('profile/', profile , name = 'profile'),
    path('logout/', logout , name = 'logout'),
    path('FAQs/<slug>', FAQs , name = 'FAQs'),
    path('about/', about , name = 'about'),

    path('contact/', contact , name = 'contact'),
    # path('footer/', footer , name = 'footer'),
    path('blog/', articleHome , name = 'articleHome'),
    path('blog/<slug>', articleView , name = 'articleView'),

    path('emi-calculator/', emi , name = 'emi'),
  
    re_path('emi-pro/', credit , name = 'credit'),
    path('emi-pro/personalDetails/', personalDetails , name = 'personalDetails'),
    path('emi-pro/submit/', submit , name = 'submit'),
    path('emi-enquiry/', EMIEnquiryFun , name = 'EMIEnquiryFun'),
    path ('Services/', getServices, name='getServices'),
    path ('Services/bankname/', BankNames, name='bankname'),
    path ('Services/statename/', StateNames, name='statename'),
    path ('Services/cityname/', CityNames, name='cityname'),
    path ('Services/branchname/', BranchNames, name='branchname'),
    path ('Services/ifscfilter/', Ifscfilter, name='ifscfilter'),
    # path ('ifsc/ifscfiller/', Ifscfiller, name='ifscfiller')
    path('Services/<slug>', Ifscfiller, name='ifscfiller'),
    path('emi-pro/apply_loan/', apply_loan, name='apply_loan'),
    path('Services/grievance/', Grievance, name='grievance'),
    path('Services/grievancefilter/', GrievanceFilter, name='grievancefilter'),

    path('income_tax_calculator', income_tax_calculator,
         name='income_tax_calculator'),
    path('income_cal', income_cal, name='income_cal')


]
