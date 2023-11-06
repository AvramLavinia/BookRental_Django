from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from sef_portal.models import *
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'sef/login.html')
    else:
        return render(request, 'sef/home_page.html')

def login(request):
    return render(request, 'sef/login.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'sef/home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            sef = Sef.objects.get(sef = user)
        except:
            sef = None
        if sef is not None:
            auth.login(request, user)
            return render(request, 'sef/home_page.html')
        else:
            return render(request, 'sef/login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'sef/login.html')

def register(request):
    return render(request, 'sef/register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    mobile = request.POST['mobile']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']

    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'sef/registration_error.html')
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        sef = Sef(sef = user, mobile = mobile, area=area)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        sef = Sef(sef = user, mobile = mobile, area=area)
    sef.save()
    return render(request, 'sef/registered.html')

@login_required
def add_book(request):
    book_name = request.POST['book_name']
    color = request.POST['color']
    cd = Sef.objects.get(sef=request.user)
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    description = request.POST['description']
    pg = request.POST['pg']
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        book = Books(book_name=book_name, color=color, dealer=cd, area = area, description = description, pg=pg)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        book = Books(book_name=book_name, color=color, dealer=cd, area = area,description=description, pg=pg)
    book.save()
    return render(request, 'sef/book_added.html')

@login_required
def manage_books(request):
    username = request.user
    user = User.objects.get(username = username)
    sef = Sef.objects.get(sef = user)
    book_list = []
    books = Books.objects.filter(dealer = sef)
    for v in books:
        book_list.append(v)
    return render(request, 'sef/manage.html', {'book_list':book_list})

@login_required
def order_list(request):
    username = request.user
    user = User.objects.get(username = username)
    sef = Sef.objects.get(sef = user)
    orders = Orders.objects.filter(sef = sef)
    order_list = []
    for o in orders:
        if o.is_complete == False:
            order_list.append(o)
    return render(request, 'sef/order_list.html', {'order_list':order_list})

@login_required
def complete(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    book = order.book
    order.is_complete = True
    order.save()
    book.is_available = True
    book.save()
    return HttpResponseRedirect('/sef_portal/order_list/')


@login_required
def history(request):
    user = User.objects.get(username = request.user)
    sef = Sef.objects.get(sef = user)
    orders = Orders.objects.filter(sef = sef)
    order_list = []
    for o in orders:
        order_list.append(o)
    return render(request, 'sef/history.html', {'wallet':sef.wallet, 'order_list':order_list})

@login_required
def delete(request):
    veh_id = request.POST['id']
    book = Books.objects.get(id = veh_id)
    book.delete()
    return HttpResponseRedirect('/sef_portal/manage_books/')
