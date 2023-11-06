from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from sef_portal.models import *
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'customer/login.html')
    else:
        return render(request, 'customer/home_page.html')

def login(request):
    return render(request, 'customer/login.html')

def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'customer/home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            customer = Customer.objects.get(user = user)
        except:
            customer = None
        if customer is not None:
            auth.login(request, user)
            return render(request, 'customer/home_page.html')
        else:
            return render(request, 'customer/login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'customer/login.html')

def register(request):
    return render(request, 'customer/register.html')

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
        return render(request, 'customer/registration_error.html')
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        customer = Customer(user = user, mobile = mobile, area = area)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        customer = Customer(user = user, mobile = mobile, area = area)

    customer.save()
    return render(request, 'customer/registered.html')

@login_required
def search(request):
    return render(request, 'customer/search.html')

@login_required
def search_results(request):
    city = request.POST['city']
    city = city.lower()
    books_list = []
    area = Area.objects.filter(city = city)
    for a in area:
        books = Books.objects.filter(area = a)
        for book in books:
            if book.is_available == True:
                book_dictionary = {'name':book.book_name, 'color':book.color, 'id':book.id, 'pincode':book.area.pincode, 'pg':book.pg, 'description':book.description}
                books_list.append(book_dictionary)
    request.session['books_list'] = books_list
    return render(request, 'customer/search_results.html')


@login_required
def rent_book(request):
    id = request.POST['id']
    book = Books.objects.get(id = id)
    cost_per_day = int(book.pg)
    return render(request, 'customer/confirmation.html', {'book':book, 'cost_per_day':cost_per_day})

@login_required
def confirm(request):
    book_id = request.POST['id']
    username = request.user
    user = User.objects.get(username = username)
    days = request.POST['days']
    book = Books.objects.get(id = book_id)
    if book.is_available:
        sef = book.dealer
        rent = (int(book.pg))+(int(days))
        sef.wallet += rent
        sef.save()
        try:
            order = Orders(book = book, sef = sef, user = user, rent=rent, days=days)
            order.save()
        except:
            order = Orders.objects.get(book = book, sef = sef, user = user, rent=rent, days=days)
        book.is_available = False
        book.save()
        return render(request, 'customer/confirmed.html', {'order':order})
    else:
        return render(request, 'customer/order_failed.html')

@login_required
def manage(request):
    order_list = []
    user = User.objects.get(username = request.user)
    try:
        orders = Orders.objects.filter(user = user)
    except:
        orders = None
    if orders is not None:
        for o in orders:
            if o.is_complete == False:
                order_dictionary = {'id':o.id,'rent':o.rent, 'book':o.book, 'days':o.days, 'sef':o.sef}
                order_list.append(order_dictionary)
    return render(request, 'customer/manage.html', {'od':order_list})

@login_required
def update_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    book = order.book
    book.is_available = True
    book.save()
    sef = order.sef
    sef.wallet -= int(order.rent)
    sef.save()
    order.delete()
    cost_per_day = int(book.pg)*1
    return render(request, 'customer/confirmation.html', {'book':book}, {'cost_per_day':cost_per_day})

@login_required
def delete_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    sef = order.sef
    sef.wallet -= int(order.rent)
    sef.save()
    book = order.book
    book.is_available = True
    book.save()
    order.delete()
    return HttpResponseRedirect('/customer_portal/manage/')
