from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member

class MemberAdmin(UserAdmin):
    model = Member
    list_display = ('reg_no', 'firstname', 'secondname', 'email',
                    'faculty', 'year_of_study', 'is_active', 'is_staff')
    search_fields = ('reg_no', 'firstname', 'secondname', 'email')
    ordering = ('reg_no',)

    # Only filter by faculty
    list_filter = ('faculty','year_of_study',)

    fieldsets = (
        (None, {'fields': ('reg_no', 'firstname',
         'secondname', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('reg_no', 'firstname', 'secondname', 'email', 'faculty', 'year_of_study', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )



admin.site.register(Member, MemberAdmin)
