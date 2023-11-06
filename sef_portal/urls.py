from django.urls import path,include
from sef_portal.views import *
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^index/$',index),
    re_path(r'^login/$',login),
    re_path(r'^auth/$',auth_view),
    re_path(r'^logout/$',logout_view),
    re_path(r'^register/$',register),
    re_path(r'^registration/$',registration),
    re_path(r'^add_book/$',add_book),
    re_path(r'^manage_books/$',manage_books),
    re_path(r'^order_list/$',order_list),
    re_path(r'^complete/$',complete),
    re_path(r'^history/$',history),
    re_path(r'^delete/$',delete),
]
