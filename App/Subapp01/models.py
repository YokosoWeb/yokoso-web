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
    
    Name = models.CharField(max_length=100)
   
    Email = models.EmailField(max_length=100)
    Phone = models.EmailField(max_length=100)
    Message = models.TextField(null=True)

    def __str__(self,):
        return self.Name + ' | '  + self.Email + ' | ' + self.Phone 



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
        return reverse('articleView', args = [self.slug])
#new
    # def get_absolute_url(self):
    #     return reverse("add_post", args=(str(self.id)))
    


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

class EMI_Data(models.Model):
      name =  models.CharField(max_length = 200, blank = True)
      phone =  models.FloatField(blank=True,null = True)
      pan =  models.CharField(max_length = 200, blank = True)
      employment = models.CharField(max_length = 200, blank = True)
      email=models.CharField(max_length = 200, blank = True)
      dob=models.CharField(max_length = 200, blank = True)
      gender=models.CharField(max_length = 200, blank = True)
  
      bank = models.CharField(max_length = 200, blank = True)
      salary=models.FloatField(max_length = 200, blank = True, null = True)
      ongoingemi =  models.FloatField(max_length = 200, blank = True ,null = True)
      loantype=models.CharField(max_length = 200, blank = True)
      tenure =models.FloatField(max_length = 200, blank = True,null = True)
    
      loanamount = models.FloatField(blank=True,null = True)
      created = models.DateTimeField(auto_now_add=True,null = True, blank = True)
       


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
    
    # ADDRESS = models.CharField(max_length=500,blank=True,null = True)

class bank_grievance(models.Model):
    babk_ifsc = models.CharField(max_length=500,blank=True,null = True)
    Bank = models.CharField(max_length = 1000, blank = True,null = True)
    level1 = models.CharField(max_length = 1000, blank = True,null = True)
    level2 = models.CharField(max_length = 500, blank = True,null = True)
    level3 = models.CharField(max_length = 500, blank = True,null = True)
    helpful_link = models.CharField(max_length = 500, blank = True,null = True)
    twitter_handle = models.CharField(max_length = 1000, blank = True,null = True)

class customer_data(models.Model):
    full_name = models.CharField(max_length=500,blank=False,null = False)
    pan_number = models.CharField(max_length=500,blank=False,null = False)
    emp_type = models.CharField(max_length=500,blank=False,null = False)
    phone_number = models.CharField(max_length=500,blank=False,null = False)
    email_address = models.CharField(max_length=500,blank=False,null = False)
    Date_of_birth = models.CharField(max_length=500,blank=False,null = False)
    gender = models.CharField(max_length=500,blank=False,null = False)


class testing(models.Model):
    name=models.CharField(max_length=500,blank=False,null = False)


class loan_Comparison(models.Model):
    bank = models.CharField(max_length = 200, blank = True)
    min_interest_rate = models.CharField(max_length = 200, blank = True)
    max_interest_rate = models.CharField(max_length = 200, blank = True)  
    processing_fees = models.CharField(max_length = 200, blank = True)
    loan_max = models.CharField(max_length = 200, blank = True)
   
    max_tenure = models.CharField(max_length = 200, blank = True)
    lowest_emi_per_lakh = models.CharField(max_length = 200, blank = True)
    benchmark_rate = models.CharField(max_length = 200, blank = True)
    current_mclr_plr=  models.CharField(max_length = 200, blank = True)
    base_rate=  models.CharField(max_length = 200, blank = True)
    min_age= models.CharField(max_length = 200, blank = True)
    max_age =  models.CharField(max_length = 200, blank = True)
    for_women =  models.CharField(max_length = 200, blank = True)
    overdraft_facilty =  models.CharField(max_length = 200, blank = True)
	
	