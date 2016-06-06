import requests
import re
from urllib.parse import urlparse
from gcmclient import JSONMessage

from django.conf import settings
from django.core.mail import send_mail

__all__ = 'notify', 'get_registrations'

GCM_PREFIX = 'https://android.googleapis.com/gcm/send/'
EMAIL_PREFIX = 'mailto:'

def url2gcm(url):
    return url[len(GCM_PREFIX):]

def gcm2url(regid):
    return GCM_PREFIX+regid

def notify(user, *, text=None, data=None):
    """
    Primary entry point to piston. Arguments are:

    1. The user object or ID
    * `text`: Human-readable text to send to any email addresses
    * `data`: Machine-readable data to send to WebPush (Unimplemented)
    """
    from .models import PushRegistration
    for pr in PushRegistration.objects.filter(user=user):
        url = pr.pushurl
        # SMTP/Email
        if url.startswith(EMAIL_PREFIX):
            do_email(url, text)
        # Because GCM is special and doesn't follow WebPush
        elif url.startswith(GCM_PREFIX):
            do_gcm(url, data)
        # And for people who do follow WebPush (aka Firefox)
        else:
            do_plainpost(pr.pushurl, data)

def do_plainpost(url, data):
    requests.post(url)
    # TODO: Handle errors

def do_gcm(url, data):
    """
    Kicks off the GCM process
    """
    from .tasks import send_gcm_message
    print("gcm", url)

    msg = JSONMessage([url2gcm(url)])
    send_gcm_message(msg)

def do_email(url, text):
    """
    NOTE: Doesn't support comma-seperated multiple email addresses
    """
    if not text:
        text = settings.PISTON_EMAIL_DEFAULT_TEXT
    email = urlparse(url).path
    # Do some special handling if it's actually a text message
    istxt = any(email.endswith(d) for d in ('@vtext.com'))  # FIXME: Get a more complete list

    subject = "" if istxt else settings.PISTON_EMAIL_SUBJECT

    send_mail(subject, text, settings.PISTON_EMAIL_FROM, [email], fail_silently=False)

def url2email(url):
    return urlparse(url).path

def email2url(email):
    return 'mailto:'+email

def get_registrations(user):
    """
    Get a sequence of tuples of the URL and the type of URL it is.
    """
    from .models import PushRegistration
    for pr in PushRegistration.objects.filter(user=user):
        t = "web"
        if pr.pushurl.startswith(EMAIL_PREFIX):
            t = "email"
        yield pr.pushurl, t