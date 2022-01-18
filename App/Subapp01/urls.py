
from django.contrib import admin
from django.urls import path, include
from .views import *



urlpatterns = [
    path('', home , name = 'home'),
    path('signin/', signin , name = 'signin'),
    path('signup/', signup , name = 'signup'),
    path('profile/', profile , name = 'profile'),
    path('logout/', logout , name = 'logout'),
    path('FAQs/<slug>', FAQs , name = 'FAQs'),
    path('about/', about , name = 'about'),
    path('contact/', contact , name = 'contact'),
    path('blog/', articleHome , name = 'articleHome'),
    path('blog/<slug>', articleView , name = 'articleView'),

    path('emi-calculator/', emi , name = 'emi'),
    
    path('emi-pro/', credit , name = 'credit'),

    path('emi-enquiry/', EMIEnquiryFun , name = 'EMIEnquiryFun'),
    path ('ifsc/', getServices, name='getServices'),
    path ('ifsc/bankname/', BankNames, name='bankname'),
    path ('ifsc/statename/', StateNames, name='statename'),
    path ('ifsc/cityname/', CityNames, name='cityname'),
    path ('ifsc/branchname/', BranchNames, name='branchname'),
    path ('ifsc/ifscfilter/', Ifscfilter, name='ifscfilter'),
    # path ('ifsc/ifscfiller/', Ifscfiller, name='ifscfiller')
    path ('ifsc/<slug>', Ifscfiller, name='ifscfiller'),
    path('grievance', Grievance, name="Grievance")
    # path('get', get , name = 'get'),
    # path('del', delete , name = 'delete')
]
