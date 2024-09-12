from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OneTimePassword, Profile, UserRolePermissions

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'telephone', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    search_fields = ('email', 'first_name', 'last_name', 'telephone')
    ordering = ('-date_joined',)  # You can still use it for ordering, just not in the fieldsets
    
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'telephone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Role', {'fields': ('role',)}),
        ('Important dates', {'fields': ('last_login',)}),  # Removed 'date_joined'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'telephone', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # New user
            UserRolePermissions.assign_permissions(obj)
        super().save_model(request, obj, form, change)

class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp')
    search_fields = ('user__email', 'otp')
    readonly_fields = ('otp',)  # Make OTP read-only if it's only for display

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date')
    search_fields = ('user__email', 'bio', 'location')
    readonly_fields = ('user',)  # Make user field read-only

# Register the models with their custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(OneTimePassword, OneTimePasswordAdmin)
admin.site.register(Profile, ProfileAdmin)
