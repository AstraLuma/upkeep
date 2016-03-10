from django.contrib import admin
from .models import Thing, Schedule, Job

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    pass

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass
