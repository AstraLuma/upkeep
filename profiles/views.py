from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from piston import get_registrations, url2email, email2url

@login_required
def index(request):
    browsers = 0
    emails = set()
    for url, typ in get_registrations(request.user):
        if typ == 'web':
            browsers += 1
        elif typ == 'email':
            emails.add(url)
    return render(request, "profiles/index.html", {
        'browsers': browsers,
        'emails': [(e, url2email(e)) for e in sorted(emails)],
        })
