import requests
import re
from gcmclient import JSONMessage

__all__ = 'notify',

GCM_PREFIX = 'https://android.googleapis.com/gcm/send/'

def url2gcm(url):
    return url[len(GCM_PREFIX):]

def gcm2url(regid):
    return GCM_PREFIX+regid

def notify(user):
    from .models import PushRegistration
    print("notify", user)
    for pr in PushRegistration.objects.filter(user=user):
        url = pr.pushurl
        print("url", url)
        if url.startswith(GCM_PREFIX):
            print("gcm")
            # Do special GCM stuff
            do_gcm(url)
        else:
            print("post")
            do_plainpost(pr.pushurl)

def do_plainpost(url):
    requests.post(url)
    # TODO: Handle errors

def do_gcm(url):
    """
    Kicks off the GCM process
    """
    from .tasks import send_gcm_message
    print("gcm", url)

    msg = JSONMessage([url2gcm(url)])
    send_gcm_message(msg)