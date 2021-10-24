from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User


from App.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.


def home(request):

    # Default Response
    objs = FAQCategory.objects.all()
    return render(request, 'app/index.html', {"objs": objs})


def signup(request):
    if request.method == "POST":
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                email = request.POST['email']
                user = User.objects.filter(email=email)
                if len(user) == 0:
                    raise User.DoesNotExist
                return render(request, 'app/signup.html', {'msg': 'Email already exists 🔑', 'c': 'red'})
            except User.DoesNotExist:
                # user = '@'+request.POST['email']
                user = '@' + str(request.POST['email'])[0:-10]
                user_obj = User.objects.create_user(
                    first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=user, password=request.POST['pass1'], email=request.POST['email'])
                print(user_obj)

                user_obj.save()
                try:
                    send(user_obj)
                except:
                    pass

                new_prof = Profile(username=user_obj,
                                   phone=request.POST.get('phone'), Gender=" ", Location="")
                new_prof.save()

                return redirect('signin')

        else:
            return render(request, 'app/signup.html', {'msg_pass': "Password do not matched ❌"})
    else:
        return render(request, 'app/signup.html')


def signin(request):
    if request.method == "POST":
        try:
            uname = request.POST['email']
            pwd = request.POST['pass1']
            print(uname, pwd)
            uname = '@'+uname[0:-10]
            uid = User.objects.get(username=uname)
            user_authenticate = auth.authenticate(username=uname, password=pwd)
            print(user_authenticate)
            if user_authenticate is not None:
                if user_authenticate.is_staff:
                    auth.login(request, user_authenticate)
                    # Code changed
                    return redirect('profile')
                else:
                    auth.login(request, user_authenticate)
                    request.session['username'] = uname
                    return redirect('profile')
            else:
                print('Login Failed')
                return render(request, 'app/signin.html', {"msg": "Invalid Credentials ❌"})
        except:
            return render(request, 'app/signin.html', {"msg": "Invalid Credentials ❌"})

    else:
        return render(request, 'app/signin.html')


def logout(request):

    uid = User.objects.get(username=request.user)

    auth.logout(request)

    if request.session.has_key('username'):
        del request.session['username']
    else:
        pass

    return redirect('signin')


def profile(request):
    try:
        user = User.objects.get(username=request.user)

        return render(request, 'app/profile.html', {'user': user})
    except:
        return redirect('signin')


def send(user_obj):
    subject, from_email = 'Welcome', EMAIL_HOST_USER
    html_content = render_to_string(
        'app/email.html', {'i': user_obj})  # render with dynamic value
    # Strip the html tag. So people can see the pure text at least.
    text_content = strip_tags(html_content)
    # create the email, and attach the HTML version as well.
    emails = user_obj.email
    to = []
    to.append(emails)

    # print(i.username.email)
    print(to)
    msg = EmailMultiAlternatives(
        subject, text_content, 'Welcome' + EMAIL_HOST_USER, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('Email ok')


def FAQs(request, slug):
    print(slug)
    category = FAQCategory.objects.get(slug=slug)
    print(category.id)
    datas = FAQText.objects.filter(category=category.id)
    print(datas)
    return render(request, 'app/faq.html', {'datas': datas})


def about(request):
    return render(request, 'app/about.html')


def contact(request):
    if request.method == 'POST':

        contactObj = Contact.objects.create(Firstname=request.POST['first_name'],
                                            Lastname=request.POST['last_name'],
                                            Email=request.POST['email'],
                                            Phone=request.POST['phone'],
                                            Message=request.POST.get('msg', ''),)
        contactObj.save()

        return render(request, 'app/contact.html', {'msg': True})

    else:
        return render(request, 'app/contact.html')


def articleHome(request):
    posts = Post.objects.filter(status='Published').order_by('date')[::-1]
    return render(request, 'app/Articles/articlesHome.html', {'posts': posts})


def articleView(request, slug):
    post = Post.objects.get(slug=slug)
    print(post)
    return render(request, 'app/Articles/articleView.html', {'post': post})


def emi(request):
    return render(request, 'app/calculator.html')
