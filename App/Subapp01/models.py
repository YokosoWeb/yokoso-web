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
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(FAQCategory, on_delete = models.CASCADE, null = True)
    
    def __str__(self):
        return self.title

