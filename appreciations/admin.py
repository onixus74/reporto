from django.contrib import admin
import reversion

from .models import *


class VersionModelAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Category, VersionModelAdmin)
admin.site.register(Report, VersionModelAdmin)
