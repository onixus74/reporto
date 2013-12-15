from django.contrib import admin
from users.models import User
from django.contrib.auth.models import Group
import reversion


class VersionModelAdmin(reversion.VersionAdmin):
    pass

# admin.site.register(User)
admin.site.register(User, VersionModelAdmin)
admin.site.unregister(Group)
# admin.site.register(Group)
admin.site.register(Group, VersionModelAdmin)


# from .forms import UserChangeForm, UserAddForm

# class CustomUserAdmin(UserAdmin):
#     add_form = UserCreationForm
#     form = UserChangeForm
