from django.contrib import admin
from .models import PushRegistration

@admin.register(PushRegistration)
class PRAdmin(admin.ModelAdmin):
    pass
