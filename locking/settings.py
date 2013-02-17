from django.conf import settings

MEDIA_URL = getattr(settings, 'MEDIA_URL', '/media/')
LOCKING_URL = getattr(settings, 'LOCKING_URL', '/locking/')
STATIC_URL = getattr(settings, 'STATIC_URL', '/static/')
