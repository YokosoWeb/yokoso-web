
from django.contrib import admin
from django.urls import path, include
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
    path('blog/', articleHome , name = 'articleHome'),
    path('blog/<slug>', articleView , name = 'articleView'),

    path('emi-calculator/', emi , name = 'emi'),
    
    path('emi-pro/', credit , name = 'credit'),

    path('emi-enquiry/', EMIEnquiryFun , name = 'EMIEnquiryFun'),
    # path ('service/', getServices, name='getServices'),

    path ('service/', getServices, name='getServices'),
 
    path ('service/getstates', getstates, name='getstates'),
    # # path ('ifscResult', ifscResult, name='ifscResult'),
    path('load_cities/', load_cities, name ='ajax_load_cities'),
    path('load_branches/', load_branches, name ='ajax_load_branches'),

    # path('get', get , name = 'get'),
    # path('del', delete , name = 'delete')
]
