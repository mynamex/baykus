# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path


from .views import home


# app_name = "home"

urlpatterns = [
    # The home page
    path('', home, name='home'),



]
