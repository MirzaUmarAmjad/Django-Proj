# Import necessary classes
import datetime

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from django.conf import settings
from .forms import OrderForm, InterestForm, LoginForm, RegisterForm, ForgotPassswordForm
from .models import Topic, Course, Student, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

# In the index function we are only passing the topic list
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


# the about function to view the about page
# In the about function we are not passing any extra context variable
def about(request):
    visits = int(request.COOKIES.get('about_visits', '0'))
    visits = visits + 1
    # set max age to 5 minutes
    maxAge = 300

    response = render(request, 'myapp/about.html', {'about_visits':visits})
    response.set_cookie('about_visits', visits,max_age=maxAge)

    return response


# detail page to view the detail by topic id and if it is not available then show 404 not found
# In the detail function we are passing the topic record and course list against that record
def detail(request, top_no):
    response = HttpResponse()
    topic = get_object_or_404(Topic, id=int(top_no))
    courseList = Course.objects.all().filter(topic__id=int(top_no))
    return render(request, 'myapp/detail.html', {'topic': topic, 'course_list': courseList})


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
                if order.course.price > 150.0:
                    order.course.discount()
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})


def coursedetail(request, cour_id):
    cour = get_object_or_404(Course, id=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['interested']
            levels = form.cleaned_data['levels']
            if interest:
                cour.interested += 1
                cour.save()
            return HttpResponseRedirect(reverse('myapp:index'))
    else:
        form = InterestForm()
        return render(request, 'myapp/coursedetail.html', {'form': form, 'cour': cour})


def user_login(request):
    if request.method == 'POST':

        # test coookie work in the browser or not
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        else:
            return HttpResponse("Please enable cookies and try again.")

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                # set session
                request.session['last_login'] = str(datetime.datetime.now())
                # set expiry to 1 hour
                request.session.set_expiry(3600)

                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        form = LoginForm()
        # set test cookie
        request.session.set_test_cookie()
        return render(request, 'myapp/login.html', {'loginform': form})


@login_required
def user_logout(request):

    logout(request)
    del request.session
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required
def myaccount(request):
    user = request.user
    msg = ""
    if user.is_staff:
        msg = "You are not a registered student!"
        return render(request, 'myapp/myaccount.html', {'msg': msg})
    else:
        order_list = Order.objects.filter(student__id=user.id)
        interested_topic = Student.objects.filter(username=user.username).values('interested_in__name')
        return render(request, 'myapp/myaccount.html',
                      {'msg': msg, 'firstname': user.first_name, 'lastname': user.last_name, 'orderlist': order_list,
                       'interestList': interested_topic})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            crtUser = form.save(commit=False)
            crtUser.save()
            u = User.objects.get(username=request.POST.get('username'))
            u.set_password(  request.POST.get('password') )
            u.save()
            return HttpResponseRedirect(reverse('myapp:user_login'))
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'registerform': form})


@login_required
def myorders(request):
    user = request.user
    msg = ""
    if user.is_staff:
        msg = "You are not a registered student!"
        return render(request, 'myapp/myorders.html', {'msg': msg})
    else:
        order_list = Order.objects.filter(student__id=user.id)
        return render(request, 'myapp/myorders.html',
                      {'msg': msg, 'orderlist': order_list})


def forgotpassword(request):
    if request.method == 'POST':
        form = ForgotPassswordForm(request.POST)
        if form.is_valid():

            u = User.objects.get(username= request.POST.get('username'))
            if u:
                u.set_password('123123')
                u.save()

                subject = 'Password Reset'
                message = 'Hi , your new password is 123123.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [u.email, ]
                send_mail(subject, message, email_from, recipient_list)

        return HttpResponseRedirect(reverse('myapp:user_login'))
    else:
        form = ForgotPassswordForm()
        return render(request, 'myapp/forgotpassword.html', {'forgotPassswordForm': form})