from django.contrib import admin
from .models import UserProfile, UserAddress
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Inline admin descriptors for UserProfile model which acts as a profile of the built-in User model


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fk_name = 'user'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('userprofile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city',
                    'state', 'zip_code', 'country', 'is_default']
    list_filter = ['country', 'is_default']
    search_fields = ['user__username', 'address', 'city', 'zip_code']
