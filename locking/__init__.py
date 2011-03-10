VERSION = (0, 3, 0)
import logging
from django.conf import settings

# Validate settings.
time_until_expiration = int(settings.LOCKING['time_until_expiration'])
time_until_warning = settings.LOCKING['time_until_warning']

if time_until_warning >= time_until_expiration:
    raise Exception("LOCKING['time_until_warning'] must be smaller than"
                    "  LOCKING['time_until_expiration']"
                    )
    
logger = logging.getLogger('django.locker')