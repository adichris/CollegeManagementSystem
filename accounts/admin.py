from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserModelAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("identity", "first_name", 'last_name', 'is_online')
    list_filter = ("is_online", 'is_active', 'is_admin', 'is_superuser')

    search_fields = ("identity", 'first_name', 'last_name', 'email')
    
    add_fieldsets = [
        ("Credentials", {"fields": ('identity', 'password'), 'classes':"wide"}),
        ("Personal Information", {"fields":('first_name', 'last_name','email', 'date_of_birth', 'gender', 'phone_number')})
    ]
    fieldsets = [
        (None, {"fields": ('identity', 'password'), 'classes':"wide"}),
        ("Personal Information", {"fields":('first_name', 'last_name','email', 'date_of_birth', 'gender', 'phone_number'), 'classes':'wide'}),
        ("Picture", {"fields": ('picture', ), 'classes':'wide'}),
        ("Permission", {'fields': ('is_admin', 'is_superuser')}),
        ("Active Status", {"fields": ("is_active", 'is_online', ), "classes": "wide"}),
        ("User Browser Information",
         {"fields": ("session_key", 'last_login', 'os', 'username', 'computer_name', 'http_sec_ch_ua'),
          "classes": "wide"}
         ),
        ("Groups and Authorization",
         {"fields": ("groups", ), "classes": "wide"}),
    ]

    readonly_fields = ('is_online', 'session_key', 'last_login', 'os', 'computer_username', 'computer_name', 'http_sec_ch_ua')
    ordering = ("first_name", "last_name", "email")
    filter_horizontal = ()
