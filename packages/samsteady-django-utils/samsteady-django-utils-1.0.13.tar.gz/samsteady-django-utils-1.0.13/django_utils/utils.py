from django.contrib.auth import get_user_model
from django.conf import settings


def is_anonymous_user(user):
    if  user is None or user.is_anonymous:
        return True
    User = get_user_model()
    username = getattr(user, User.USERNAME_FIELD)
    if hasattr(settings, 'ANONYMOUS_USER_NAME'):
        anon_username = settings.ANONYMOUS_USER_NAME

    else:
        from guardian.conf import settings as guardian_settings
        anon_username = guardian_settings.ANONYMOUS_USER_NAME
    return anon_username and anon_username == username
