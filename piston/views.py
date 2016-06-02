from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings
import json
from .models import PushRegistration


@login_required
def addurl(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Try a POST'}, status=405)  # Method Not Allowed
    obj = json.loads(request.body.decode('utf-8'))
    if 'url' not in obj:
        return JsonResponse({'msg': 'Missing URL'}, status=400)

    pr = PushRegistration()
    pr.user = request.user
    pr.pushurl = obj['url']
    try:
        pr.save()
    except IntegrityError:
        # Probably duplicate URL for the user
        pass

    return JsonResponse({}, status=202)  # Accepted

@login_required
def dropurl(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Try a POST'}, status=405)  # Method Not Allowed
    obj = json.loads(request.body.decode('utf-8'))
    if 'url' not in obj:
        return JsonResponse({'msg': 'Missing URL'}, status=400)

    pr = PushRegistration.objects.get(user=request.user, pushurl=obj['url'])

    if not pr:
        return JsonResponse({}, status=200)

    pr.delete()

    return JsonResponse({}, status=200)

def manifest(request):
    m = getattr(settings, 'WEB_MANIFEST', {}).copy()
    if hasattr(settings, 'GCM_SENDER_ID'):
        m['gcm_sender_id'] = settings.GCM_SENDER_ID
    return JsonResponse(m)