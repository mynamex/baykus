import uuid

import shortuuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.accounts.models import Account, Apartments, Devices
from apps.customauth.models import MyUser
from apps.home.serializer import DevicesSerializer, ApartmentsSerializer
from apps.home.views import eD
from apps.staff.decarator import admin_only
from apps.staff.forms import EditCustomerForm, CreateCustomerForm
from apps.staff.serializers import UserSerializer

from utils.query_debuger import query_debugger

my_decorators = [query_debugger, admin_only, login_required(login_url='auth:login')]


# client.married = True if request.PUT.get("married") == 'true' else False
def is_true_or_false(val):
    if str(val).lower() == "false":
        return False
    elif str(val).lower() == "true":
        return True


def get_customer_detail(pk_customer):
    account = Account.objects.prefetch_related("apartments").get(id=pk_customer)
    users = MyUser.objects.filter(account=account, is_active=True)

    context = {
        'customer': account,
        'user_count': len(users),
        'apartments_count': len(account.apartments.all()),
    }
    return context


# --------------------------------------------------------------------------------------------------------
# -----------------  Customer ---------------Customer------------------Customer-----------------Customer----
# --------------------------------------------------------------------------------------------------------


@login_required(login_url='auth:login')
@admin_only
def createCustomer(request):
    load_template = request.path

    msg = None
    success = False

    if request.method == "POST":
        form = CreateCustomerForm(request.POST)
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
        form = CreateCustomerForm()

    return render(request, "staff/customer_temp/create-customer.html",
                  {"form": form, "segment": load_template, "msg": msg, "success": success})


@query_debugger
@login_required(login_url='auth:login')
@admin_only
def editCustomerInfo(request, pk_test):
    # account = Account.objects.get(id=pk_test)
    account = Account.objects.prefetch_related("blocks", "apartments", "gates").get(id=pk_test)
    form = EditCustomerForm(instance=account)

    if request.method == 'POST':
        form = EditCustomerForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            # return redirect('/')
            # messages.add_message(request, messages.INFO, 'Baarılı.')
            # account = Account.objects.prefetch_related("blocks", "apartments", "gates").get(id=pk_test)

            context = {'customer': account,
                       'blocks': account.blocks.all(),
                       'blocks_count': len(account.blocks.all()),
                       'daire_count': len(account.apartments.all()),
                       'gates_count': len(account.gates.all()),
                       "dairies": account.apartments.all(),
                       "gates": account.gates.all(),
                       "show_block_detail": False,
                       'myFilter': []}
            return render(request, 'staff/customer_temp/customer.html', context)
        else:
            messages.add_message(request, messages.INFO, 'Baarısız.')

    # modul_types = ModuleTypeSerializerStaff(ModuleType.objects.all(), many=True)
    context = {'customer': account, "form": form}
    return render(request, 'staff/customer_temp/edit-customer_form.html', context)


@query_debugger
@login_required(login_url='auth:login')
@admin_only
def customer(request, pk_customer):
    context = get_customer_detail(pk_customer)
    context["go_to"] = "customer_main"
    return render(request, 'staff/customer_temp/customer.html', context)


# --------------------------------------------------------------------------------------------------------
# -----------------  Users ---------------Users------------------Users-----------------Users-------------
# --------------------------------------------------------------------------------------------------------


@method_decorator(my_decorators, name='dispatch')
class CustUsersView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.success = True

    def get(self, request):

        try:
            users = MyUser.objects.filter(account_id=request.GET.get('account_id')).prefetch_related("account")

            self.data["d_users"] = UserSerializer(users, many=True).data
        except Exception as err:
            self.data["desc"] = str(err)
            self.success = False

        return JsonResponse({"success": self.success, "data": self.data})

    def to_json(self, objects):
        return serializers.serialize('json', objects)

    def post(self, request):
        try:
            with transaction.atomic():
                if request.POST.get("in_go") == "update":
                    account = Account.objects.get(pk=request.POST.get('account_id'))

                    user = MyUser.objects.get(pk=request.POST.get('user_id'), account=account)
                    user.account = account
                    user.name = eStrip(request.POST.get('name')).title()
                    user.username = eStrip(request.POST.get('username'))

                    user.is_active = is_true_or_false(request.POST.get('is_active'))

                    if not request.POST.get("password") == "********":
                        if 5 < len(request.POST.get("password")) < 10:
                            user.set_password(request.POST.get("password"))
                        else:
                            self.data["desc"] = "Uygun parola olmalı (en az 6 hafr en fazla 10)"
                            return JsonResponse({"success": False, "data": self.data})

                    user.save()
                    self.data["desc"] = "Kullanıcı Güncellendi"

                elif request.POST.get("in_go") == "create":
                    newuser = MyUser.objects.create(
                        account=Account.objects.get(pk=request.POST.get('account_id')),
                        name=eStrip(request.POST.get('name')).title(),
                        username=eStrip(request.POST.get('username')),
                        is_active=True)

                    newuser.set_password(request.POST.get('password'))
                    newuser.save()

                    self.data["added_id"] = newuser.pk
                    self.data["desc"] = "Yeni Kullanıcı Eklendi"

        except IntegrityError as e:
            if str(e).__contains__("UNIQUE"):
                self.data["desc"] = "Bu kullanıcı adı zatenkullanılıyor"
            else:
                self.data["desc"] = str(e)
            self.success = False

        except Exception as err:
            self.data["desc"] = str(err)
            self.success = False

        return JsonResponse({"success": self.success, "data": self.data})


@login_required(login_url='auth:login')
@admin_only
def customerUsers(request, pk_customer):
    context = get_customer_detail(pk_customer)
    context["go_to"] = "show_customer_users"
    return render(request, 'staff/customer_temp/customer.html', context)


def eStrip(val):
    return str(val).strip()


# --------------------------------------------------------------------------------------------------------
# -----------------  Gates ---------------Gates------------------Gates-----------------Gates------------
# --------------------------------------------------------------------------------------------------------


@query_debugger
@login_required(login_url='auth:login')
@admin_only
def ShowCampus(request, pk_customer):
    context = get_customer_detail(pk_customer)
    context["go_to"] = "show_campus"

    return render(request, 'staff/customer_temp/customer.html', context)


@method_decorator(my_decorators, name='dispatch')
class StaffCampusView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apartment = None
        self.success = True

        self.family = None
        self.data = {"desc": ""}
        self.user = None

    def post(self, request):

        try:
            with transaction.atomic():
                account = Account.objects.get(pk=request.POST.get("account_id", ""))

                if request.POST.get("in_go") == "get_apartments":
                    d_apartments = Apartments.objects.filter(account=account)
                    return JsonResponse({"d_apartments": ApartmentsSerializer(d_apartments, many=True).data})

                if request.POST.get("in_go") == "update":

                    ap = Apartments.objects.get(pk=request.POST.get("ap_id", None), account=account)
                    ap.name = eD(self.request.POST.get("name", ""))
                    ap.wifi_name = self.request.POST.get("wifi_name", "")
                    ap.wifi_pass = self.request.POST.get("wifi_pass", "")
                    ap.address = eD(self.request.POST.get("address", ""))
                    ap.is_active = is_true_or_false(self.request.POST.get("is_active", None))
                    ap.save()

                    self.data["desc"] = "cihaz güncellendi"

                elif request.POST.get("in_go") == "create":
                    new_apartments = Apartments.objects.create(
                        account=account,
                        name=request.POST.get('name'),
                        api_key=shortuuid.uuid(),
                        wifi_name=self.request.POST.get("wifi_name", ""),
                        wifi_pass=self.request.POST.get("wifi_pass", ""),
                        address=request.POST.get('address', "")
                    )

                    c1 = new_apartments.device.create(
                        key="temp",
                        name="Isı",
                        device_type="input")

                    c2 = new_apartments.device.create(
                        key="humid",
                        name="Nem",
                        device_type="input")

                    c3 = new_apartments.device.create(
                        key="amlight",
                        name="Ortam aydınlığı",
                        device_type="input")

                    c4 = new_apartments.device.create(
                        key="pir_sensor",
                        name="Hareket",
                        device_type="input")

                    c5 = new_apartments.device.create(
                        key="buzzer",
                        name="Buzzer",
                        device_type="output")

                    c6 = new_apartments.device.create(
                        key="flash_light",
                        name="Işık yak",
                        device_type="output")

                    c7 = new_apartments.device.create(
                        key="alarm",
                        name="Alarm",
                        device_type="output")

                    new_apartments.devices.add(c1, c2, c3, c4, c5, c6, c7)
                    new_apartments.save()

                    self.data["desc"] = "yeni yerleşke oluşturuldu"
                    self.data["new_apartments_id"] = new_apartments.pk

        except Account.DoesNotExist:
            self.data["desc"] = "Bu müşteri bulunamadı"
            self.success = False

        except IntegrityError as e:
            if str(e).__contains__("UNIQUE"):
                if str(e).__contains__("users_carplates.name"):
                    self.data["desc"] = "Bu yerleşke zaten kayıtlı"
                elif str(e).__contains__("accounts_device.key"):
                    self.data["desc"] = "default cihazlardan birtanesinin keyi kullanılıyor"
                else:
                    self.data["desc"] = "Zaten var"

            else:
                self.data["desc"] = str(e)
            self.success = False

        except Exception as err:

            self.data["desc"] = str(err)

            self.success = False

        return JsonResponse({"success": self.success, "data": self.data})


@query_debugger
@login_required(login_url='auth:login')
@admin_only
def showApartments(request, pk_customer):
    account = Account.objects.get(id=pk_customer, salesman=request.user)

    context = {'go_to': "show_apartments", "customer": account}
    return render(request, 'staff/customer_temp/customer.html', context)


@method_decorator(my_decorators, name='dispatch')
class DevicesView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apartment = None
        self.success = True

        self.family = None
        self.data = {"desc": ""}
        self.user = None

    def get(self, request):

        try:
            apartment = Apartments.objects.get(account=request.GET.get("account_id", None),
                                               pk=request.GET.get("ap_id", None))

            self.data["d_data"] = DevicesSerializer(apartment.devices.all(), many=True).data

        except Apartments.DoesNotExist:
            self.data["desc"] = "Yerleşke Bulunamadı"
            self.success = False

        except Exception as err:
            self.data["desc"] = str(err)
            self.success = False

        return JsonResponse({"success": self.success, "data": self.data})

    def post(self, request):

        try:
            with transaction.atomic():

                apartment = Apartments.objects.get(pk=request.POST.get("ap_id", None))

                if request.POST.get("in_go") == "update":

                    ap = apartment.device.get(pk=request.POST.get("dev_id", None))

                    ap.name = eD(self.request.POST.get("name", ""))
                    ap.key = self.request.POST.get("key", "")
                    ap.device_type = self.request.POST.get("device_type", "")
                    ap.status = is_true_or_false(request.POST.get("status", None))
                    ap.is_active = is_true_or_false(request.POST.get("is_active", None))
                    ap.save()

                    apartment.save()

                    self.data["desc"] = "cihaz güncellendi"

                elif request.POST.get("in_go") == "create":
                    new_device = Devices.objects.create(

                        apartment=apartment,
                        name=eD(self.request.POST.get("name", "")),
                        key=self.request.POST.get("key", ""),
                        device_type=self.request.POST.get("device_type", "")
                    )

                    new_device.save()
                    apartment.devices.add(new_device)

                    self.data["desc"] = "Yeni bir cihaz yaratıldı"
                    self.data["new_devices_id"] = new_device.pk

        except IntegrityError as e:
            if str(e).__contains__("UNIQUE"):
                if str(e).__contains__("accounts_device.key"):
                    self.data["desc"] = "Bu key kullanılıyor"
                elif str(e).__contains__("accounts_device.name"):
                    self.data["desc"] = "Bu cihaz adı kullanılıyor"
                else:
                    self.data["desc"] = "Zaten var" + str(e)
            else:
                self.data["desc"] = str(e)

            self.success = False

        except Exception as err:
            self.data["desc"] = str(err)
            self.success = False

        return JsonResponse({"success": self.success, "data": self.data})
