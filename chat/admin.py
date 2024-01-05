from django.contrib import admin

from .models import Group, ActivePeriod

# Register your models here.
admin.site.register(Group)
admin.site.register(ActivePeriod)
