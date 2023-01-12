

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.customauth.models import MyUser
from .form import ShowAccountUserForm, UserCreationForm, UserChangeForm
from .models import Account


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'is_admin', 'is_staff')
    list_filter = ('account',)
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        ('Personal info', {'fields': ('account',)}),
        # ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'username',  'password1', 'password2', 'account'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    def has_delete_permission(self, request, obj=None):
        return False


class AccountsAdmin(admin.TabularInline):
    model = MyUser
    extra = 1
    form = ShowAccountUserForm
    readonly_fields = ('name', 'username',)

    # def has_add_permission(self, request, obj):
    #     return False


# class BlocksAdmin(admin.TabularInline):
#     model = Blocks
#     extra = 1


# class GatenameAdmin(admin.TabularInline):
#     model = GateName
#     extra = 1


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    fields = ('name', 'related_person_name',
              'phone', 'licence_date')

    list_display = ('name',
                    'related_person_name', 'licence_date', 'license_status')
    list_editable = ("license_status",)

    list_filter = (
        ('license_status', admin.BooleanFieldListFilter),
    )


    # inlines = [AccountsAdmin, GatenameAdmin, BlocksAdmin]
    inlines = [AccountsAdmin]

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
# ------------------------------------
# Blocks

#
# class DaireForm(forms.ModelForm):
#     daire_name = forms.CharField()
#
#
#     def clean(self):
#         cleaned_data = super().clean()
#         try:
#             daire_name = cleaned_data["daire_name"]
#
#             customer = self.instance
#             account = self.instance.account
#
#             print("block name : {}  account id : {}  ".format(customer,  account))
#
#             if Daire.objects.filter(daire_name=daire_name,
#                                     customer=customer,
#                                     account=account).exists():
#
#                 raise forms.ValidationError("unique !")
#             else:
#
#                 daire = Daire(daire_name=daire_name,  account=account,  customer=customer)
#                 daire.save()
#                 return cleaned_data
#         except KeyError as err:
#             return cleaned_data
#
#     class Meta:
#         model = Daire
#         exclude = ['daire_name',]


# class DaireAdmin(admin.TabularInline):
#     readonly_fields = ('account', 'daire_name')
#     fields = ('daire_name', 'daire_status', 'account')
#
#     model = Daire
#     extra = 0
#
#     def has_add_permission(self, request, obj):
#         return False


# @admin.register(Blocks)
# class BlocksAdmin(admin.ModelAdmin):
#     save_on_top = True
#     readonly_fields = ('account', 'block_name')
#     list_filter = ("account",)
#     inlines = [DaireAdmin, ]
#
#     form = DaireForm
#
#     def save_model(self, request, obj, form, change):
#
#         # block_id = obj.id
#         # employee_id = obj.employee.pk
#         # daire_name = form.cleaned_data["daire_name"]
#
#         super().save_model(request, obj, form, change)
#
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#
#         form.base_fields["daire_name"].label = "Daire name"
#
#         return form
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def has_add_permission(self, request):
#         return False
