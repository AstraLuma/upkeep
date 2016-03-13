from tasks import task
from gcmclient import GCM, JSONMessage
from django.conf import settings
from . import gcm2url, url2gcm

_gcm = None

@task
def send_gcm_message(msg):
    global _gcm
    if _gcm is None:
        _gcm = GCM(settings.GCM_APIKEY)

    print("GCM Send", msg)

    result = _gcm.send(msg)

    # Some kind of remapping
    for oldreg, newreg in result.canonical.items():
        try:
            pr = PushRegistration.objects.get(pushurl=gcm2url(oldreg))
        except PushRegistration.DoesNotExist:
            continue
        else:
            pr.pushurl = gcm2url(newreg)
            pr.save()

    # Registration removed
    for regid in result.not_registered:
        try:
            pr = PushRegistration.objects.get(pushurl=gcm2url(regid))
        except PushRegistration.DoesNotExist:
            continue
        else:
            pr.delete()

    # Permanent failure
    for regid, errcode in result.failed.items():
        try:
            pr = PushRegistration.objects.get(pushurl=gcm2url(regid))
        except PushRegistration.DoesNotExist:
            continue
        else:
            pr.delete()

    # Retries
    if result.needs_retry():
        retrymsg = result.retry()
        dly = result.delay(retrymsg)
        send_gcm_message.retry(retrymsg, countdown=dly)
