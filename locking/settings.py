from django.conf import settings


MEDIA_URL = getattr(settings, 'MEDIA_URL', '/media/')
LOCKING_URL = getattr(settings, 'LOCKING_URL', '/locking/')
STATIC_URL = getattr(settings, 'STATIC_URL', '/static/')

LOCKING_SETTINGS = getattr(settings, 'LOCKING', {})

TIME_UNTIL_EXPIRATION = LOCKING_SETTINGS.get('time_until_expiration', 600)
TIME_UNTIL_WARNING = LOCKING_SETTINGS.get('time_until_warning', 540)
