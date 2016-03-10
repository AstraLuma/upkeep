from social.backends.google import GoogleOAuth2
from social.backends.facebook import FacebookOAuth2

def associate_by_email(backend, response, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.

    This pipeline entry is not 100% secure unless you know that the providers
    enabled enforce email verification on their side, otherwise a user can
    attempt to take over another user account by using the same (not validated)
    email address on some provider.  This pipeline entry is disabled by
    default.
    """
    if user:
        return None

    # FIXME: Handle multiple emails
    #   Google: response['emails'][...]['value']
    #   Facebook: ???

    email = details.get('email')
    if email:
        # Check to see if the backend verified the email
        print(backend, response)
        verified = False
        if isinstance(backend, GoogleOAuth2):
            # response['emails'][...]['isVerified'], except it's missing for me?
            # Different endpoint than implemented by default -_-
            pass
        elif isinstance(backend, FacebookOAuth2):
            verified = True  # TODO: Double check this

        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = list(backend.strategy.storage.user.get_users_by_email(email))
        if len(users) == 0:
            return None
#        elif len(users) > 1:
        else:
            raise AuthException(
                backend,
                'The given email address is associated with another account'
            )
#        else:
#            return {'user': users[0]}
