from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings
import json
from .models import PushRegistration
from . import EMAIL_PREFIX, WEBPUSH_PREFIXES, do_email

# Constant for session storage, used by the confirmation logic
SESSION_CODE = 'piston.confirmation-code'
SESSION_URL = 'piston.confirmation-url'

# Confirmation workflow:
# * If WebPush, accept without problems
# 1. If email, reject registration with HTTP 428. Server sends code to email and saves it and the email in 
#    session storage
# 2. User gives code to web app. App resends the registration with the url and confirmation code (as `code`)
# 3. If URL and code match, server accepts registration
# Errors:
# * If URL does not match, server acts as if no URL was saved and starts new workflow
# * Each session can only have one active registration process at a time (FIXME)
# * If URL matches but code does not match, HTTP 412 is returned
# * If the URL matches and code is saved, but code is not given, server again restarts and generates a new code

def generate_confirmation_code():
    ...

@login_required
def addurl(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Try a POST'}, status=405)  # Method Not Allowed
    obj = json.loads(request.body.decode('utf-8'))
    if 'url' not in obj:
        return JsonResponse({'msg': 'Missing URL'}, status=400)

    url = obj['url']

    if any(url.startswith(pf for pf in WEBPUSH_PREFIXES):
        # Pass through without problems
        pass
    elif url.startswith(EMAIL_PREFIX):
        # Logic to check for a code for this url
        if SESSION_CODE not in request.session or url != request.session.get(SESSION_URL) or 'code' not in obj:
            code = generate_confirmation_code()
            request.session[SESSION_URL] = url
            request.session[SESSION_CODE] = code
            do_email(url, "Confirmation code: {}\n\n(If you didn't ask for this, you may safely ignore.)".format(code))
            return JsonResponse({'msg': 'Requires confirmation code'}, status=428)  # An abuse of 428 Precondition Required
        if obj['code'] != request.session[SESSION_CODE]:
            return JsonResponse({'msg': 'Missing confirmation code'}, status=412)  # An abuse of 412 Precondition failed

        # Code is valid for this URL
        assert request.session.get(SESSION_CODE) == obj['code'] and request.session.get(SESSION_URL) == url

        # Clean up
        del request.session[SESSION_URL]
        del request.session[SESSION_CODE]

        # And pass through
    else:
        # Unrecognized URL. Reject to prevent DoS-type abuse
        return JsonResponse({'msg': 'Unrecognized URL'}, status=406)  # Abuse of 406 Unacceptable

    pr = PushRegistration()
    pr.user = request.user
    pr.pushurl = url
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