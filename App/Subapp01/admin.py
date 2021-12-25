from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(FAQCategory)
admin.site.register(FAQText)
admin.site.register(EMIEnquiry)
admin.site.register(ADV_EMI_CAL)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Branch)
admin.site.register(Bank)
admin.site.register(Ifscdetails)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields= ('title','content')

