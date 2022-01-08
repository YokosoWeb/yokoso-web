from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.





# User Account Models

# User Have - Firstname,Lastname,username,email,password and Profile is connected to user
# User Profile
class Profile(models.Model):
    Gender = models.CharField(max_length=20,null = True)
    phone = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    username = models.ForeignKey(User , on_delete = models.CASCADE)

    def __str__(self):
        return str(self.username.first_name) + " " + str(self.username.last_name)



class Contact(models.Model):
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Phone = models.EmailField(max_length=100)
    Message = models.TextField(null=True)

    def __str__(self,):
        return self.Firstname + ' ' +  self.Lastname + ' | ' + self.Email + ' | ' + self.Phone 



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.CharField(max_length = 100,null = True, blank = True)
    description = models.CharField(max_length =100)
    icon = models.CharField(max_length = 100)

    def __str__(self,):
        return self.name



class EMIEnquiry(models.Model):
    name = models.CharField(max_length = 100,null = True, blank = True)
    phone = models.CharField(max_length = 100,null = True, blank = True)
    pan = models.CharField(max_length = 100,null = True, blank = True)
    email = models.CharField(max_length =100,null = True, blank = True)
    dob = models.CharField(max_length = 100,null = True, blank = True)
    gender = models.CharField(max_length = 100,null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True,null = True, blank = True)

    def __str__(self,):
        return self.name



class Post(models.Model):
    STATUS_CHOICES=(('Draft','Draft'),('Published','Published'),)
    title=models.CharField(max_length=250,unique=True)
    meta = models.TextField(blank=True)
    date=models.DateField(auto_now=True)
    content=RichTextField(blank=True,null=True)
    author=models.ForeignKey(Profile,on_delete=models.CASCADE)
    slug=models.SlugField(unique=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='Draft')
    category=models.ManyToManyField(Category,related_name='category')
    image=models.ImageField(upload_to='images/',blank=True)

    
    def __str__(self):
        return self.title



    def get_absolute_url(self):
        return reverse("add_post", args=(str(self.id)))
    


# FAQs Models

class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length = 100)

    def __str__(self):
        return self.name



class FAQText(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(FAQCategory, on_delete = models.CASCADE, null = True)
    
    def __str__(self):
        return self.title
class ADV_EMI_CAL(models.Model):
    cal_id = models.IntegerField(primary_key=True)
    bank = models.CharField(max_length = 200, blank = True)
    loan_type = models.CharField(max_length =500, blank = True)
    feature_type = models.CharField(max_length =500, blank = True)
    gender = models.CharField(max_length=500, blank = True)
    cibil_min = models.IntegerField(blank = True)
    cibil_max = models.IntegerField(blank = True)
    loan_min = models.IntegerField(blank = True)
    loan_max = models.IntegerField(blank = True)
    interest_rate = models.FloatField(blank = True)


class IfscData(models.Model):
    IFSC_CODE = models.CharField(max_length=200,blank=True,null = True)
    BANK = models.CharField(max_length = 200, blank = True,null = True)
    STATE = models.CharField(max_length = 200,blank=True,null = True)
    DISTRICT = models.CharField(max_length = 200,blank=True,null = True)
    CITY = models.CharField(max_length = 200,blank=True)
    BRANCH = models.CharField(max_length = 200,blank=True,null = True)
    PHONE = models.FloatField(blank=True,null = True)
    STD_CODE = models.FloatField(blank=True,null = True)
    MICR = models.FloatField(blank=True,null = True)
    ADDRESS = models.CharField(max_length=500,blank=True,null = True)