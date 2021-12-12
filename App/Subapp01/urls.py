
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

    path('emi-enquiry/', EMIEnquiryFun , name = 'EMIEnquiryFun')

    # path('get', get , name = 'get'),
    # path('del', delete , name = 'delete')
]
