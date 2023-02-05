# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path


from .views import home, aparts,  Apis, WatchCampus, getApartments, custWatch

# app_name = "home"

urlpatterns = [
    # The home page
    path('', home, name='home'),
    path('cust_watch/', custWatch, name="cust_watch"),
    path('get_apartments/', getApartments, name="get_apartments"),

    path('aparts/<str:pk_apart>/', aparts, name="aparts"),

    path('watch_campus/', WatchCampus.as_view(), name="watch_campus"),


    # path('role_view/', RoleView.as_view(), name="role_view"),

    path('apis/', Apis, name="apis"),


]
