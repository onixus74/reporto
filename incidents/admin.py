from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

admin.site.register(Category)
# admin.site.register(Feature)
admin.site.register(Feature, MPTTModelAdmin)
admin.site.register(Media)
admin.site.register(Victim)
admin.site.register(Comment)
admin.site.register(Report)
