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
def is_valid_queryparam(param):
    return param != '' and param is not None

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


def credit(request):
    # data = ADV_EMI_CAL.objects.all()
    # print(data.count())
    if request.method == 'POST':
        BANK_FOIR = 70
        name = request.POST['fname']
        pan = request.POST['pan']
        employment = request.POST['emp']
        phone = request.POST['phone']
        email = request.POST['email']
        dob = request.POST['dob']
        gender = request.POST.get('gender')

        monthlySalary = request.POST.get('ms')
        ongoingEmi = request.POST.get('oe', 0)
        loanType = request.POST.get('loanType')
        loanAmount = request.POST.get('la')
        tenure = request.POST.get('month')
        bank = request.POST.get('bankName')
        creditScore = request.POST.get('creditScore')

        print(name, pan, employment, phone, email, dob, gender)
        print(monthlySalary, ongoingEmi, loanType,
              loanAmount, tenure, bank, creditScore)

        EMI_MAX = (int(monthlySalary) - int(ongoingEmi))*(0.70)
        print(EMI_MAX)
        DefaultROI = 6.25

        P1 = (1+float(DefaultROI)) ** int(tenure)
        print(P1)
        r = float(DefaultROI)/(12*100)
        p = int(loanAmount)
        n = int(tenure)

        # Calculating Equated Monthly Installment (EMI)
        EMI_REAL = round(p * r * ((1+r)**n)/((1+r)**n - 1), 2)

        #  LOAN_MAX and EMI_MAX, Tenure , ROI
        LOAN_MAX = round(EMI_MAX * float(tenure))
        ROI = DefaultROI
        TENURE = n
        LOAN_REAL = loanAmount

        # Less Loan Real ( Not eligible for Loan )
        if int(LOAN_MAX) < int(LOAN_REAL):
            return render(request, 'app/emi-pro-output.html', {'EMI_MAX': EMI_MAX, 'LOAN_MAX': LOAN_MAX,'eligible' :False})


        # Process on DB
        data = ADV_EMI_CAL.objects.filter(feature_type=employment).filter(
            loan_type=loanType)
        print(data.count())

        loan__amount = (int(int(loanAmount)/100000))
        data1 = []
        for i in data:
            if (loan__amount >= i.loan_min) and (loan__amount <= i.loan_max):
                data1.append(i)
            print(i.bank,i.loan_type,i.loan_min,i.loan_max,)



        # if not show then show others


        print(len(data1))
        data2 = []
        if creditScore:
            creditScore = creditScore
        else:
            creditScore = 900
        for i in data1:
            if (int(creditScore) >= i.cibil_min) and ( int(creditScore) <= i.cibil_max): 
                data2.append(i)
                print(i.cal_id,i.bank,i.loan_type,i.loan_min,i.loan_max,i.cibil_min,i.cibil_max,i.gender)
        print(data2)
        data3 = []

        

        for i in data2:
            # print(type(gender)==type(i.gender))
            # print(gender,i.gender)
            if str(i.gender) == gender:
                data3.append(i)
            elif str(i.gender) == 'Other' or str(i.gender) == 'None':
                data3.append(i)

        for i in data3:
            print(i.cal_id,i.bank,i.loan_type,i.loan_min,i.loan_max,i.cibil_min,i.cibil_max,i.gender)
        print(data3)


     


        # print(int(int(loanAmount)/100000))

        return render(request, 'app/emi-pro-output.html', {'EMI_MAX': EMI_MAX, 'EMI_REAL': EMI_REAL, 'LOAN_MAX': LOAN_MAX, 'LOAN_REAL': LOAN_REAL, 'ROI': ROI, 'TENURE': TENURE,'eligible' :True, 'data' : data3})
    return render(request, 'app/creditScore.html')


def EMIEnquiryFun(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pan = request.POST.get('pan')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')

        # obj = EMIEnquiry(name=name, email=email, gender=gender,
        # pan=pan, phone=phone,dob=dob)
        # obj.save()
        print(name)
        return HttpResponse(name)


def ifscfilter(request):
    
    qs = Ifscdetails.objects.all()
    state_names = State.objects.all
    city_names = City.objects.all()
    branch_names = Branch.objects.all()
    bank_names =Bank.objects.all()
    state = request.GET.get('state')
    city = request.GET.get('city')
    branch = request.GET.get('branch')
    bankname = request.GET.get('bankname')
    ifsc_no_exact_query = request.GET.get('ifsc_no_exact')
    if is_valid_queryparam(ifsc_no_exact_query): 
        qs = qs.filter(ifsc_no = ifsc_no_exact_query)
    if is_valid_queryparam(city) and city != 'Choose...':
        qs = qs.filter(city_names__name = city)
    if is_valid_queryparam(state) and state != 'Choose...':
        qs = qs.filter(state_names__name = state)
    if is_valid_queryparam(bankname) and bankname != 'Choose...':
        qs = qs.filter(bank_names__name = bankname)
    if is_valid_queryparam(branch) and branch != 'Choose...':
        qs = qs.filter(branch_names__name = branch_names)
       
    context = {
        'queryset': qs,
        'state_names': state_names,
        'city_names': city_names,
        'bank_names': bank_names,
        'branch_names': branch_names,
      
       
     }
    # print(city_names)
    # print(state_names)
    # print(bank_names)
    # print(branch_names)
    # # print(ifsc_no_contains)
    # print(qs)
    return render(request, "app/ifsc_code.html", context)

def load_cities(request):
    state_id = request.GET.get('state')
    # cityes = City.objects.filter(state_id=state_id).all()
    cities = City.objects.filter(state_id=state_id).order_by('name')
    print(cities)
    return render(request, 'app/city_dropdown_list_options.html', {'cities': cities})

def load_branches(request):
    city_id = request.GET.get('city')
    # cityes = City.objects.filter(state_id=state_id).all()
    branches = Branch.objects.filter(city_id=city_id).order_by('name')
    print(branches)
    return render(request, 'app/branch_dropdown_list_options.html', {'branches': branches})
