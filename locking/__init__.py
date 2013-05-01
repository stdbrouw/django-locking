VERSION = (0, 3, 0)

from django.conf import settings
import urls

#TODO: LOCK_TIMEOUT isn't being used anymore, clean it up throughout the code
LOCK_TIMEOUT = getattr(settings, 'LOCK_TIMEOUT', 1800)
