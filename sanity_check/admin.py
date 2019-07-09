from django.contrib import admin
from sanity_check.models import Site, Check


admin.site.register(Site)
admin.site.register(Check)
# Register your models here.
