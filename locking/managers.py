import datetime

from django.db import models
from django.db.models import Q

from locking import LOCK_TIMEOUT

class LockManager(models.Manager):
    def locked(self):
        now = datetime.datetime.now()
        qs = super(LockManager, self).get_query_set()
        qs = qs.extra(select={'expires_at':'DATE_ADD(locked_at,INTERVAL 120 SECOND)'})
        qs = qs.extra(where=['DATE_ADD(locked_at,INTERVAL %s SECOND) > %s'], params=[LOCK_TIMEOUT, now])
        return qs

    def unlocked(self):
        now = datetime.datetime.now()
        qs = super(LockManager, self).get_query_set()
        qs = qs.extra(select={'expires_at':'DATE_ADD(locked_at,INTERVAL 120 SECOND)'})
        qs = qs.extra(where=['DATE_ADD(locked_at,INTERVAL %s SECOND) < %s or locked_at IS NULL'], params=[LOCK_TIMEOUT, now])
        return qs

    def locked_for(self, user):
        qs = super(LockManager, self).get_query_set()
        qs = qs.extra(select={'expires_at':'DATE_ADD(locked_at,INTERVAL 120 SECOND)'})
        qs = qs.extra(where=['DATE_ADD(locked_at,INTERVAL %s SECOND) > %s'], params=[LOCK_TIMEOUT, now])
        qs = qs.filter(_locked_by = user)
        return qs