from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.customauth.models import MyUser


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):

        user = MyUser.objects.get(id=request.user.pk)

        if user.is_salesman:

            return view_func(request, *args, **kwargs)
        else:
            return redirect('unauthorized')

    return wrapper_function


def cust_admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            user = MyUser.objects.get(id=request.user.pk, is_active=True)
        except MyUser.DoesNotExist:
            return HttpResponse('Bu kişi bulunamadı !')

        if user.is_person:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('unauthorized')

    return wrapper_function

from django.db import connection
from django.db import reset_queries


def database_debug(func):
    def inner_func(*args, **kwargs):
        reset_queries()
        results = func()
        query_info = connection.queries
        print('function_name: {}'.format(func.__name__))
        print('query_count: {}'.format(len(query_info)))
        queries = ['{}\n'.format(query['sql']) for query in query_info]
        print('queries: \n{}'.format(''.join(queries)))
        return results
    return inner_func