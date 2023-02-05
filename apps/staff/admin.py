
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib import admin
from apps.staff.admin_form import UserChangeForm, UserCreationForm
from apps.customauth.models import MyUser
from apps.staff.models import Log


class MyStaff(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_admin', 'is_salesman', 'is_active')
    list_filter = ('account', 'is_salesman')
    fieldsets = (
        (None, {'fields': ('username', 'name', 'is_active')}),
        ('Personal info', {'fields': ('is_salesman',)}),
        # ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'username',  'is_salesman', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Log)

admin.site.register(MyUser, MyStaff)