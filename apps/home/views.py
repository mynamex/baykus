# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.models import Account, Apartments, Devices, Role
from apps.customauth.models import MyUser
from apps.home.form import CreateApartments
from apps.home.serializer import ApartmentsSerializer, DevicesSerializer, RoleSerializer
from django.db import IntegrityError, transaction

from utils.query_debuger import query_debugger

my_decorators = [query_debugger, login_required(login_url='login')]


def is_true_or_false(val):
    if val == "false":
        return False
    elif val == "true":
        return True


def is_NONE(val):
    if val is None:
        return False
    else:
        return True


# @method_decorator(my_decorators, name='dispatch')
@query_debugger
@login_required(login_url='auth:login')
def home(request):
    user = MyUser.objects.select_related("account").get(username=request.user)
    context = {"segment": "home", "customer": Account.objects.get(id=user.account_id)}
    html_template = loader.get_template('staff/staff-index.html')
    return HttpResponse(html_template.render(context, request))

    # if user.is_person:
    #     # context = get_cust_customer_detail(request.user.pk)
    #
    #     context = {"segment": "home", "customer": Account.objects.get(id=user.account_id, license_status=True)}
    #     html_template = loader.get_template('cust_users/cust-index.html')
    #     return HttpResponse(html_template.render(context, request))
    #
    # elif not user.is_person:
    #     html_template = loader.get_template('home/page-no-official-user.html')
    #     return HttpResponse(html_template.render({"context": "siz bir ofis görevlisi değilsiniz !"}, request))


@login_required(login_url='auth:login')
def createApart(request):
    load_template = request.path

    msg = None
    success = False

    if request.method == "POST":
        form = CreateApartments(request.POST)
        if form.is_valid():
            new_account = form.save()
            new_account.salesman = request.user
            new_account.save()
            # site_name = form.cleaned_data.get("site_name")
            # tax_number = form.cleaned_data.get("tax_number")
            # related_person_name = form.cleaned_data.get("related_person_name")
            # site_phone1 = form.cleaned_data.get("site_phone1")
            # site_address = form.cleaned_data.get("site_address")
            # licence_date = form.cleaned_data.get("licence_date")
            return HttpResponseRedirect('/')


        else:
            msg = 'Form düzngün oluşturulunamadı'
    else:
        form = CreateApartments()

    return render(request, "staff/customer_temp/create-apart.html",
                  {"form": form, "segment": load_template, "msg": msg, "success": success})


@query_debugger
@login_required(login_url='auth:login')
def aparts(request, pk_customer):
    account = Account.objects.get(pk=request.POST.get('account_id'))
    apartments = Apartments.objects.get(account=account)
    context = {
        'account': account,
        "apartments": apartments
    }
    return render(request, 'staff/customer_temp/customer.html', context)


@method_decorator(my_decorators, name='dispatch')
class ApartmentsView(View):

    def get(self, request):
        user = MyUser.objects.get(username=request.user)

        d_apartments = Apartments.objects.filter(account=user.account)

        return JsonResponse({"d_apartments": ApartmentsSerializer(d_apartments,many=True).data})

    def post(self, request):
        user = MyUser.objects.select_related("account").get(username=request.user.username)

        if request.POST.get("in_go") == "update":
            try:

                ap = Apartments.objects.get(pk=request.POST.get("ap_id", None))
                ap.name = eD(self.request.POST.get("name", ""))
                ap.wifi_name = self.request.POST.get("wifi_name", "")
                ap.wifi_pass = self.request.POST.get("wifi_pass", "")
                ap.address = eD(self.request.POST.get("address", ""))
                ap.is_active = is_true_or_false(self.request.POST.get("is_active", None))
                ap.save()

                return JsonResponse({"result": True}, safe=False)

            except IntegrityError as e:
                if str(e).__contains__("UNIQUE"):
                    return JsonResponse({"result": False, "status_message": "Bu kullanıcı adı zatenkullanılıyor"},
                                        safe=False)
                else:
                    return JsonResponse({"result": False, "status_message": str(e)}, safe=False)
            except Exception as err:
                print(err)
                return JsonResponse({"result": False, "status_message": err}, safe=False)

        elif request.POST.get("in_go") == "create":
            try:

                new_apartments = Apartments.objects.create(
                    account=Account.objects.get(pk=user.account.pk),
                    name=request.POST.get('name'),
                    wifi_name=self.request.POST.get("wifi_name", ""),
                    wifi_pass=self.request.POST.get("wifi_pass", ""),
                    address=request.POST.get('address', ""))

                new_apartments.save()

                return JsonResponse({"result": True, "new_apartments_id": new_apartments.pk})

                # return JsonResponse({"result": True}, safe=False)

            except IntegrityError as e:

                return JsonResponse({"result": False, "status_message": "Bu  kullanıcı daha önce tanımlanmış"},
                                    safe=False)
            except Exception as err:
                return JsonResponse({"result": False, "status_message": err}, safe=False)


@method_decorator(my_decorators, name='dispatch')
class DevicesView(View):

    def get(self, request):
        user = MyUser.objects.get(username=request.user)

        apartment = Apartments.objects.get(account=user.account, pk=request.GET.get("ap_id", None))

        d_devices = Devices.objects.filter(apartments=apartment)

        return JsonResponse({"d_data": DevicesSerializer(d_devices, many=True).data})

    def post(self, request):
        user = MyUser.objects.select_related("account").get(username=request.user.username)

        apartment = Apartments.objects.get(pk=request.POST.get("ap_id", None), account=user.account)

        # d_devices = Devices.objects.filter(apartments=user.account.apartments)

        if request.POST.get("in_go") == "update":
            try:
                ap = Devices.objects.get(pk=request.POST.get("dev_id", None))
                ap.name = eD(self.request.POST.get("name", ""))
                ap.is_active = is_true_or_false(request.POST.get("is_active", None))
                ap.save()

                return JsonResponse({"result": True}, safe=False)

            except IntegrityError as e:
                if str(e).__contains__("UNIQUE"):
                    return JsonResponse({"result": False, "status_message": "cihaz adı zaten kullanılıyor"},
                                        safe=False)
                else:
                    return JsonResponse({"result": False, "status_message": str(e)}, safe=False)
            except Exception as err:
                print(err)
                return JsonResponse({"result": False, "status_message": err}, safe=False)

        elif request.POST.get("in_go") == "create":
            try:

                new_devices = Devices.objects.create(
                    apartments=apartment,
                    name=eD(request.POST.get("name", ""))
                )

                new_devices.save()
                return JsonResponse({"result": True, "new_devices_id": new_devices.pk})

                # return JsonResponse({"result": True}, safe=False)

            except IntegrityError as e:
                return JsonResponse({"result": False, "status_message": "Bu  cihaz adı daha önce tanımlanmış"},
                                    safe=False)
            except Exception as err:
                return JsonResponse({"result": False, "status_message": err}, safe=False)

@method_decorator(my_decorators, name='dispatch')
class RoleView(View):

    def get(self, request):
        user = MyUser.objects.get(username=request.user)

        d_devices = Role.objects.filter(devices_id=request.GET.get("device_id", None))


        return JsonResponse({"d_data": RoleSerializer(d_devices, many=True).data})

    def post(self, request):

        dev = Devices.objects.get(pk=request.POST.get("device_id", None))

        if request.POST.get("in_go") == "update":
            try:
                ap = Role.objects.get(pk=request.POST.get("role_id", None))
                ap.name = eD(request.POST.get("name", ""))
                ap.is_active = is_true_or_false(request.POST.get("is_active", None))
                ap.save()

                return JsonResponse({"result": True}, safe=False)

            except IntegrityError as e:
                if str(e).__contains__("UNIQUE"):
                    return JsonResponse({"result": False, "status_message": "cihaz adı zaten kullanılıyor"},
                                        safe=False)
                else:
                    return JsonResponse({"result": False, "status_message": str(e)}, safe=False)
            except Exception as err:
                print(err)
                return JsonResponse({"result": False, "status_message": err}, safe=False)

        elif request.POST.get("in_go") == "create":
            try:

                new_role = Role.objects.create(
                    devices=dev,
                    name=eD(request.POST.get("name", ""))
                )

                new_role.save()
                return JsonResponse({"result": True, "new_role_id": new_role.pk})

                # return JsonResponse({"result": True}, safe=False)

            except IntegrityError as e:
                return JsonResponse({"result": False, "status_message": "Bu  cihaz adı daha önce tanımlanmış"},
                                    safe=False)
            except Exception as err:
                return JsonResponse({"result": False, "status_message": err}, safe=False)


def eD(val):
    return str(val).strip().lower()

@csrf_exempt
def Apis(request):

    print("----------",request.headers["Api-Key"])
    print("----------", request.headers["Data"])

    return JsonResponse(
        {"result": False, "karagoz": "134t"}, safe=False)