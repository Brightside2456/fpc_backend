from django.contrib import admin
from .models import CustomUserModel, AddressModel
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    fieldsets = UserAdmin.fieldsets + (
        # (None, {'fields' : (
        #     'phone', 'referal_code'
        # )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        # (None, {'fields' : (
        #     'phone', 'referal_code'
        # )}),
    )
    def save_model(self, request, obj, form, change):
        if not obj.pk and obj.password:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
    pass
class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUserModel, CustomUserAdmin)
admin.site.register(AddressModel, AddressAdmin)
#  (None, {'fields': ('region', 'station_name', 'address', 'station_loc_long', 'station_loc_lat', 'station_contact')}),