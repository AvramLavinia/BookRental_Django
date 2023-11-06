from django.urls import path,include
from django.urls import include, re_path
from home.views import *
from sef_portal import *
from customer_portal import *

urlpatterns = [
    re_path(r'^$',home_page),
]
