import datetime

from django.db import models
from django.db.models import Q

from locking import LOCK_TIMEOUT

class LockManager(models.Manager):
    def locked(self):
        timeout_delta = datetime.timedelta(seconds=LOCK_TIMEOUT)
        timeout = datetime.datetime.now() - timeout_delta
        qs = super(LockManager, self).get_query_set()
        qs = qs.filter(_locked_at__gte=timeout)
        return qs

    def unlocked(self):
        timeout_delta = datetime.timedelta(seconds=LOCK_TIMEOUT)
        timeout = datetime.datetime.now() + timeout_delta
        qs = super(LockManager, self).get_query_set()
        qs = qs.filter(Q(_locked_at__lte=timeout) | Q(_locked_at__isnull=True))
        return qs

    def locked_for(self, user):
        timeout_delta = datetime.timedelta(seconds=LOCK_TIMEOUT)
        timeout = datetime.datetime.now() - timeout_delta
        qs = super(LockManager, self).get_query_set()
        qs = qs.filter(_locked_at__gt=timeout)
        qs = qs.filter(_locked_by = user)
        return qs