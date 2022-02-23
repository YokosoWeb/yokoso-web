from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(FAQCategory)
admin.site.register(FAQText)
admin.site.register(EMIEnquiry)
admin.site.register(ADV_EMI_CAL)
admin.site.register(IfscData)
admin.site.register(bank_grievance)
admin.site.register(customer_data)
admin.site.register(EMI_Data)
admin.site.register(testing)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields= ('title','content')

