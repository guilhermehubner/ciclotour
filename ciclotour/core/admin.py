from ciclotour.core.models.custom_user import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ['name', 'last_name', 'email', 'profile_picture']


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ['name', 'last_name', 'email', 'profile_picture']

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ['name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    ordering = ['name', 'last_name']
    search_fields = ('name', 'last_name', 'email')

    fieldsets = (
        (None, {'fields': ['email', 'password']}),
        ('Personal Info', {'fields': ['name', 'last_name', 'profile_picture']}),
        ('Control Fields', {'fields': ['is_active', 'is_staff', 'is_superuser']})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'last_name', 'password1', 'password2', 'profile_picture'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
