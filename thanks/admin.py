from django.contrib import admin
from incidents.models import *
import reversion


class VersionModelAdmin(reversion.VersionAdmin):
    pass

admin.site.register(ThankCategory, VersionModelAdmin)
admin.site.register(ThankReport, VersionModelAdmin)
