from django.contrib import admin
from mptt.admin import MPTTModelAdmin
import reversion

from .models import *


class VersionModelAdmin(reversion.VersionAdmin):
    pass


class VersionMPTTModelAdmin(reversion.VersionAdmin, MPTTModelAdmin):
    pass


admin.site.register(Category, VersionModelAdmin)
# admin.site.register(Feature)
admin.site.register(Feature, VersionMPTTModelAdmin)
admin.site.register(Victim, VersionModelAdmin)
admin.site.register(Comment, VersionModelAdmin)
admin.site.register(Report, VersionModelAdmin)
