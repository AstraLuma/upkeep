from django.contrib import admin
from .models import Thing, Schedule, Job

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'thing', 'period', 'next_job_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['name', 'when', 'done']
