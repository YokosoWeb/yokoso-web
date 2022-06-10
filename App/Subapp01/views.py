from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse

from App.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from math import ceil
import numpy_financial as npf
from babel.numbers import format_currency
# Create your views here.


def is_valid_queryparam(param):
    return param != '' and param is not None

def servicesview(request):
    return render(request, 'app/services.html')
def home(request):

    # Default Response
    objs = FAQCategory.objects.all()
    posts = Post.objects.filter(status='Published').order_by('date')[::-1]
    slug = "home-loan"
    category = FAQCategory.objects.get(slug=slug)
    print(category.id)
    # Entry.objects.filter()[:1].get()
    datas = FAQText.objects.filter(category=category.id)[:6]
    # datas = FAQText.objects.filter(category=category.id)
    print(datas)

    # return render(request, '../templates/index.html', {'posts': posts})

    return render(request, 'app/index.html', {"objs": objs, "posts": posts, "datas": datas})


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
    return render(request, 'app/faq.html', {'datas': datas, 'category': category})


def about(request):
    return render(request, 'app/about.html')


def contact(request):
    if request.method == 'POST':

        Firstname = request.POST.get('first_name')

        Email = request.POST.get('email')
        Phone = request.POST.get('phone')
        Category = request.POST.get('category')
        Message = request.POST.get('msg')

        context = {
            'Firstname': Firstname,

            'Email': Email,
            'Phone': Phone,
            'Category': Category,
            'Message': Message,

        }
        Message = '''
        New message: {}

        From: {}
        Contact:{}
        FirstName: {}
        Category: {}
     
        '''.format(context['Message'], context['Email'], context['Phone'], context['Firstname'], context['Category'])
        send_mail('Contact form of YOKOSO', Message, '', ['contact@yokoso.in'])

    # return render(request, 'app/contact.html', {'msg': True})

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


def apply_loan(request):
    return render(request, 'app/apply_loan.html')


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
        interest_rate = request.POST.get('interest_rate')
        data_new = ADV_EMI_CAL.objects.all().order_by('interest_rate')[0]
        DefaultROI = data_new.interest_rate

        print(name, pan, employment, phone, email, dob, gender)
        print(monthlySalary, ongoingEmi, loanType,
              loanAmount, tenure, bank, creditScore)

        EMI_MAX = (int(monthlySalary) - int(ongoingEmi))*(0.70)
        print(EMI_MAX)
        # DefaultROI = 6.25

        P1 = (1+float(DefaultROI)) ** int(tenure)
        print(P1)
        r = float(DefaultROI)/(12*100)
        p = int(loanAmount)
        n = int(tenure)

        # Calculating Equated Monthly Installment (EMI)
        EMI_REAL = round(p * r * ((1+r)**n)/((1+r)**n - 1))
        LOAN_MAX = round(
            npf.pv((DefaultROI)/1200, int(tenure), int(EMI_MAX) * -1))
        # LOAN_MAX = npf.pmt(DefaultROI/12, tenure, loanAmount)*-1
        #  LOAN_MAX and EMI_MAX, Tenure , ROI
        # LOAN_MAX = round(EMI_MAX * float(tenure))
        ROI = DefaultROI
        TENURE = n
        LOAN_REAL = loanAmount
        if creditScore:
            creditScore = creditScore
        else:
            creditScore = 900

        # Less Loan Real ( Not eligible for Loan )
        if int(LOAN_MAX) < int(LOAN_REAL):
            return render(request, 'app/emi-pro-output.html', {'EMI_MAX': EMI_MAX, 'LOAN_MAX': LOAN_MAX, 'eligible': False})

        # Process on DB
        # data = ADV_EMI_CAL.objects.filter(feature_type=employment | feature_type.isnull=True).filter(loan_type=loanType)
        data = ADV_EMI_CAL.objects.all().order_by('interest_rate')
        # print(data.count())

        # loan__amount = (int(int(loanAmount)/100000))

        data1 = []
        for i in data:
            # print("=====",i)
            if ((int(loanAmount) >= i.loan_min) and (int(loanAmount) <= i.loan_max)) and ((int(creditScore) >= i.cibil_min) and (int(creditScore) <= i.cibil_max)) and (str(i.gender).upper() == gender.upper() or i.gender is None) and (str(i.feature_type).upper() == employment.upper() or i.feature_type is None):
                data1.append(i)
        #     print(i.bank,i.loan_type,i.loan_min,i.loan_max,i.interest_rate)
        # print(data1)
        # for i in data1:
        #     print(i.cal_id,i.bank,i.loan_type,i.loan_min,i.loan_max,i.cibil_min,i.cibil_max,i.gender)
        # print("=================loan_max",i.loan_max,int(i.loan_max))
        # if not show then show others

        '''print(len(data1))
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
                data3.append(i)'''

        # for i in data3:
        #     print(i.cal_id,i.bank,i.loan_type,i.loan_min,i.loan_max,i.cibil_min,i.cibil_max,i.gender)
        # print(data3)

        # print(int(int(loanAmount)/100000))

        return render(request, 'app/emi-pro-output.html', {'EMI_MAX': format_currency((EMI_MAX), 'INR', locale='en_IN')[:-3], 'EMI_REAL': EMI_REAL, 'LOAN_MAX': format_currency((LOAN_MAX), 'INR', locale='en_IN')[:-3], 'LOAN_REAL': format_currency(LOAN_REAL, 'INR', locale='en_IN')[:-3], 'ROI': round(ROI, 2), 'TENURE': TENURE, 'eligible': True, 'data': data1[:5]})
    return render(request, 'app/creditScore.html')


def personalDetails(request):
    print("name")
    name = request.GET.get('name')
    pan = request.GET.get('pan')
    phone = request.GET.get('phone')
    employment = request.GET.get('employmentType')
    email = request.GET.get('email')
    dob = request.GET.get('dob')
    gender = request.GET.get('gender')

    obj = EMI_Data(name=name, pan=pan, phone=phone,
                   employment=employment, email=email, dob=dob, gender=gender)
    obj.save()

    return JsonResponse(obj.id, safe=False)


def submit(request):
    print("name")
    ide = request.GET.get('ide')
    la = request.GET.get('la')
    bank = request.GET.get('bank')
    salary = request.GET.get('salary')
    emi = request.GET.get('emi')
    loanType = request.GET.get('loanType')
    tenure = request.GET.get('tenure')

    print(tenure)
    ans = EMI_Data.objects.filter(id=ide).update(
        loanamount=la, bank=bank, salary=salary, ongoingemi=emi, loantype=loanType, tenure=tenure)
    print(ans)
    data = [{
        'data': ['success']}
    ]

    return JsonResponse(data, safe=False)


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

# def IfscData(re)


def getServices(request):
    context = {
        'services': ['IFSC Code', 'Grievance']
    }
    return render(request, "app/ifsc_code.html", context)


def BankNames(request):
    BankName = IfscData.objects.values_list(
        'BANK', flat=True).distinct().order_by('BANK')
    return JsonResponse(list(BankName.values('BANK')), safe=False)


def StateNames(request):
    bankname = request.GET.get('bank')
    state_names = IfscData.objects.filter(
        BANK=bankname).distinct().order_by('STATE')
    return JsonResponse(list(state_names.values('STATE')), safe=False)


def CityNames(request):
    statename = request.GET.get('state')
    bankname = request.GET.get('bank')
    city_names = IfscData.objects.filter(
        STATE=statename, BANK=bankname).distinct().order_by('CITY')
    return JsonResponse(list(city_names.values('CITY')), safe=False)


def BranchNames(request):
    cityname = request.GET.get('city')
    statename = request.GET.get('state')
    bankname = request.GET.get('bank')
    branch_names = IfscData.objects.filter(
        CITY=cityname, STATE=statename, BANK=bankname).distinct().order_by('BRANCH')
    return JsonResponse(list(branch_names.values('id', 'BRANCH')), safe=False)


def Ifscfilter(request):
    branchname = request.GET.get('branch')
    ifsc_names = IfscData.objects.filter(id=branchname)
    context = {
        'ifsc_names': ifsc_names
    }
    return render(request, "app/ifsc_code.html", context)


def Ifscfiller(request, slug):
    ifsc_no = slug  # request.GET.get('ifsc_no')
    ifsc_no = ifsc_no.upper()
    ifsc_names = IfscData.objects.filter(IFSC_CODE=ifsc_no)
    context = {
        'ifsc_names': ifsc_names
    }
    return render(request, "app/ifsc_code.html", context)



def loan_comparison(request):
    bankdetails = loan_Comparison.objects.all().distinct('bank').order_by('bank')
    print(bankdetails)
    context= {
        'bankdetails': bankdetails,
     }
    
    return render(request, 'app/loan_comparison.html', context)
 
def loan_comparisonOutput(request):
    ans = request.GET.getlist('ans[]')
    valu = request.GET.getlist('valu[]')
    print("ans")
    response1= ans[0]
    response2 = ans[1]
    ans3 = loan_Comparison.objects.filter(id=response1)
    ans4 = loan_Comparison.objects.filter(id=response2)
    # ans = request.GET.get('col2')[:1]
    print(ans3)
    # print(ans4)
    print("insideviews")
    print(valu)
    print("baove is value")
    context={
       'ans3': ans3,
       'ans4': ans4,
 }
    
    return render(request, 'app/loan_comparison.html', context)


def Grievance(request):
    # BankName = bank_grievance.objects.all()
    BankName = bank_grievance.objects.values_list(
        'Bank', flat=True).distinct().order_by('Bank')
    print("BANKNAME:", BankName)
    return JsonResponse(list(BankName.values('id', 'Bank')), safe=False)


def GrievanceFilter(request):
    bankname = request.GET.get('bank')
    grievance = bank_grievance.objects.filter(id=bankname)
    context = {
        'grievance': grievance
    }
    return render(request, "app/ifsc_code.html", context)


def income_tax_calculator(request):
    print("what's up")
    return render(request, "app/income_22.html")




def sip(request):
    print("print sip")

    return render(request, "app/sip.html")


def sipans(request):
    amount = int(request.GET.get('amount'))
    rate = eval(request.GET.get('rate'))
    time_period = int(request.GET.get('time_period'))

    month = time_period * 12
    periodic_rate = rate/100/12
    invested_amount = amount*month
    maturity = round(amount*((pow(1+periodic_rate, month)-1) /
                             periodic_rate)*(1+periodic_rate))

    data = {'invested_amount': invested_amount, 'maturity': maturity}
    
    return JsonResponse(data, safe=False)


def sipgoal(request):
    print("print sipgoal")

    return render(request, "app/sipgoal.html")


def sipgoalans(request):
    print("insidesip")
    amount = int(request.GET.get('amount'))
    rate = eval(request.GET.get('rate'))
    time_period = int(request.GET.get('time_period'))

    emi = round((amount * ((rate / 100) / 12)) /
                (pow((1 + ((rate / 100) / 12)), (time_period * 12)) - 1))
    data = {
      'amount': amount, 
      'rate': rate, 
        'time': time_period, 
        'emi': emi
}
    print("outside")
    # return render(request, "app/sipgoal.html", context)
    return JsonResponse(data, safe=False)


def lump(request):
    print("print lump")

    return render(request, "app/lump.html")


def lumpans(request):
    amount = int(request.GET.get('amount'))
    rate = eval(request.GET.get('rate'))
    time_period = int(request.GET.get('time_period'))
    maturity = amount
    for i in range(time_period):
        maturity += ((maturity*rate)/100)

    data = {'invested_amount': amount, 'maturity': round(maturity)}
    return JsonResponse(data, safe=False)


def lumpgoal(request):
    print("print lumpgoal")

    return render(request, "app/lumpgoal.html")


def lumpgoalans(request):
    amount = int(request.GET.get('amount'))
    rate = eval(request.GET.get('rate'))
    time_period = int(request.GET.get('time_period'))
    # maturity = amount
    # for i in range(time_period):
    #     maturity += ((maturity*rate)/100)
    term = pow((1+(rate/100)), time_period)
    emi = round(amount/term)

    data = {'invested_amount': amount, 'maturity': emi}
    return JsonResponse(data, safe=False)




def income_cal(request):
   
    age = request.POST['age']
    print(age)
    city = request.POST['City']
    income_from_salary = request.POST['Salary']
    basic_pay = request.POST['basicpay']
    hra = request.POST['hra']

    professional_tax = request.POST['tax']
    if professional_tax=="":
        professional_tax = 0
    capital_gain = request.POST['capital']
    if capital_gain=="":
        capital_gain = 0
    income_from_other_sources = request.POST['income']    
    if income_from_other_sources=="":
        income_from_other_sources = 0
    house_rent_annual = request.POST['rent']   
    if house_rent_annual=="":
        house_rent_annual=0
        
    # print(age,city,income_from_salary,basic_pay,hra,professional_tax)
    invest_80c = int(request.POST['80c'])
    if invest_80c == "":
        invest_80c=0
    invest_80ccd = int(request.POST['80ccd'])  
    if invest_80ccd == "":
        invest_80ccd=0
    invest_80d_self = int(request.POST['80d'])
    if invest_80d_self == "":
        invest_80d_self=0
    invest_80d_parent = int(request.POST['80d_parent'])   
    if invest_80d_parent=="":
        invest_80d_parent=0
    parent_age = int(request.POST['80d_parent_age'])
    invest_80e = int(request.POST['inv'])
    if invest_80e=="":
        invest_80e=0
    invest_24 = int(request.POST['24'])
    if invest_24 == "":
        invest_24=0
    invest_80G = int(request.POST['80g'])
    if invest_80G=="":
        invest_80G=0

    # Standard Deduction in Taxation
    std_deducation = int(50000)
    print(age,city,income_from_salary,basic_pay,hra,professional_tax,capital_gain,income_from_other_sources,house_rent_annual,
    invest_80c,invest_80ccd,invest_80e,invest_24,invest_80G)

    # Investment under Section 80C (ELSS+EPF)
    # if age<60:
    invest_80c = 150000 if invest_80c >= 150000 else invest_80c
    invest_80ccd = 50000 if invest_80ccd >= 50000 else invest_80ccd

    invest_80d_self = 25000 if int(invest_80d_self) >= 25000 else int(invest_80d_self)
    if parent_age<60:

        invest_80d_parent = 25000 if invest_80d_parent >= 25000 else invest_80d_parent
    else:
        invest_80d_parent = 50000 if invest_80d_parent >= 50000 else invest_80d_parent

    if city == 'Mumbai' or city == 'Delhi' or city == 'Kolkata' or city == 'Bangalore':
        hra_bp = (int(basic_pay))*.5
    else:
        hra_bp = float(basic_pay)*.4
    hra_rent = int(house_rent_annual) - 0.10*int(basic_pay)
    hra_exp = min(int(hra),hra_bp,hra_rent)
    gross_income = income_from_salary#+capital_gain+income_from_other_sources
    # print("=====",gross_income)
    standard_deduction = 50000
    total_exemption_old = hra_exp+standard_deduction
    total_exemption__new = 0
    invest_80e = 25000 if invest_80e >= 25000 else invest_80e
    invest_80G = 25000 if invest_80G >= 25000 else invest_80G  
    total_deduction_old = invest_80c+invest_80ccd+invest_80d_self+invest_80d_parent+invest_80e+invest_80G
    total_deduction_new = 0 
    taxable_income_old = int(gross_income) - int(total_exemption_old) - int(total_deduction_old)
    taxable_income_new = int(gross_income)

    # if taxable_income_new <= 250000:  #2 Lakh 50 thousand
    inc_tax_new = 0
    inc_tax_old = 0
    if taxable_income_new <= 500000: #5 Lakh
        inc_tax_new = 0
        inc_tax_new_slab = '0%' 
        inc_tax_new_base = 0
        inc_tax_new_slab_tax = 0

    elif taxable_income_new <= 750000: #7 lakh 50 thousand54
        inc_tax_new = (taxable_income_new - 500000) * 0.10 + 12500  
        inc_tax_new_slab = '10%' 
        inc_tax_new_base = 12500
        inc_tax_new_slab_tax = (taxable_income_new - 500000) * 0.10
    elif taxable_income_new <= 1000000: #10 Lakh
        inc_tax_new = (taxable_income_new - 750000) * 0.15 + 37500 
        inc_tax_new_slab = '15%' 
        inc_tax_new_base = 37500
        inc_tax_new_slab_tax = (taxable_income_new - 750000) * 0.15
    elif taxable_income_new <= 1250000: #12 lakh 50 thousand
        inc_tax_new = (taxable_income_new - 1000000) * 0.20 + 75000
        inc_tax_new_slab = '20%' 
        inc_tax_new_base = 75000
        inc_tax_new_slab_tax = (taxable_income_new - 1000000) * 0.20

    elif taxable_income_new <= 1500000: #15 lakh
        inc_tax_new = (taxable_income_new - 1250000) * 0.25 + 125000
        inc_tax_new_slab = '25%' 
        inc_tax_new_base = 125000
        inc_tax_new_slab_tax = (taxable_income_new - 1250000) * 0.25

    else:
        inc_tax_new = (taxable_income_new - 1500000) * 0.30 + 187500
        inc_tax_new_slab = '30%' 
        inc_tax_new_base = 187500
        inc_tax_new_slab_tax = (taxable_income_new - 1500000) * 0.30


    if int(age)<60:
        if taxable_income_old<=500000:
            inc_tax_old = 0
            inc_tax_old_slab = '0%' 
            inc_tax_old_base = 0
            inc_tax_old_slab_tax = 0


        elif taxable_income_old <= 1000000: #7 lakh 50 thousand
            inc_tax_old = (taxable_income_old - 500000) * 0.20 + 12500
            inc_tax_old_slab = '20%' 
            inc_tax_old_base = 12500
            inc_tax_old_slab_tax = (taxable_income_new - 500000) * 0.20


        elif taxable_income_old > 1000000: #7 lakh 50 thousand
            inc_tax_old = (taxable_income_old - 1000000) * 0.30 + 112500
            inc_tax_old_slab = '30%' 
            inc_tax_old_base = 112500
            inc_tax_old_slab_tax = (taxable_income_old - 1000000) * 0.30

    elif 60<=int(age)<=80:
        if taxable_income_old<=500000:
            inc_tax_old = 0
            inc_tax_old_slab = '0%' 
            inc_tax_old_base = 0
            inc_tax_old_slab_tax = 0



        elif taxable_income_old <= 1000000: #7 lakh 50 thousand
            inc_tax_old = (taxable_income_old - 500000) * 0.20 + 10000
            inc_tax_old_slab = '20%' 
            inc_tax_old_base = 10000
            inc_tax_old_slab_tax = (taxable_income_old - 500000) * 0.20


        elif taxable_income_old > 1000000: #7 lakh 50 thousand
            inc_tax_old = (taxable_income_old - 1000000) * 0.30 + 110000
            inc_tax_old_slab = '30%' 
            inc_tax_old_base = 110000
            inc_tax_new_slab_tax = (taxable_income_old - 1000000) * 0.30


    elif int(age)>80:
        if taxable_income_old<=500000:
            inc_tax_old = 0
            inc_tax_old = 0
            inc_tax_old_slab = '0%' 
            inc_tax_old_base = 0
            inc_tax_old_slab_tax = 0


        elif taxable_income_old <= 1000000: #7 lakh 50 thousand
            inc_tax_old = (taxable_income_old - 500000) * 0.20
            inc_tax_old_slab = '20%' 
            inc_tax_old_base = 0
            inc_tax_old_slab_tax = (taxable_income_old - 500000) * 0.20


        elif taxable_income_old > 1000000: #7 lakh 50 thousand
            inc_tax_old = (taxable_income_old - 1000000) * 0.30 + 100000
            inc_tax_old_slab = '30%' 
            inc_tax_old_base = 100000
            inc_tax_old_slab_tax = (taxable_income_old - 1000000) * 0.30


    if int(age)<60:
        age_value = 'below 60 years'
    else:
        age_value = 'above 60 years'

    cess_old = (inc_tax_old_base+inc_tax_old_slab_tax)*0.04
    cess_new = (inc_tax_new_base+inc_tax_new_slab_tax)*0.04




    # print(gross_income,taxable_income_old,taxable_income_new,inc_tax_old,inc_tax_new)
    return render(request, "app/income_33.html", {'Total_income': gross_income,
                                            'Professional_Tax': professional_tax,
                                            'Total_exemption_old': total_exemption_old,
                                            'total_exemption__new':total_exemption__new,
                                            'total_deduction_old': total_deduction_old,
                                            'Taxable_Income_new': taxable_income_new,
                                            'Taxable_Income_old': taxable_income_old,
                                            'total_deduction_new':total_deduction_new,
                                            'Income_Tax_old': inc_tax_old,
                                            'Income_Tax_new': inc_tax_new,
                                            'inc_tax_old_slab' : inc_tax_old_slab, 
                                            'inc_tax_old_base' : inc_tax_old_base,
                                            'inc_tax_old_slab_tax' : inc_tax_old_slab_tax,
                                            'inc_tax_new_slab' : inc_tax_new_slab, 
                                            'inc_tax_new_base' : inc_tax_new_base,
                                            'inc_tax_new_slab_tax' : inc_tax_new_slab_tax,
                                            'age_value':age_value,
                                            'cess_old':cess_old,
                                            'cess_new':cess_new

                                            })






