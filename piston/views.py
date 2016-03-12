from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import PushRegistration
from django.db import IntegrityError


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
    raise NotImplementedError()
