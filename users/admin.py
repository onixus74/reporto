from django.contrib import admin
from users.models import User
from django.contrib.auth.models import Group

admin.site.register(User)
admin.site.unregister(Group)
admin.site.register(Group)


# from .forms import UserChangeForm, UserAddForm

# class CustomUserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     form = UserChangeForm
