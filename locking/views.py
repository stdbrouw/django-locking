import simplejson

from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse

from locking.decorators import user_may_change_model, is_lockable, log
from locking import utils, LOCK_TIMEOUT, logger
from locking.models import Lock, ObjectLockedError
import locking.settings as _s

"""
These views are called from javascript to open and close assets (objects), in order
to prevent concurrent editing.
"""

@log
@user_may_change_model
@is_lockable
def lock(request, app, model, id):
    if request.user and id and app and model:
        try:
            obj = Lock.objects.get(entry_id=id, app=app, model=model)
            obj.lock_for(request.user)
            obj.save()
            return HttpResponse(status=200)
        except Lock.DoesNotExist:
            try:
                obj = Lock()
                obj.entry_id = id
                obj.app = app
                obj.model= model
                obj.lock_for(request.user)
                obj.save()
                return HttpResponse(status=200)
            except ObjectLockedError:
                # The user tried to overwrite an existing lock by another user.
                # No can do, pal!
                return HttpResponse(status=403)
    else:
        return HttpResponse(status=200)

@log
@user_may_change_model
@is_lockable
def unlock(request, app, model, id):
    # Users who don't have exclusive access to an object anymore may still
    # request we unlock an object. This happens e.g. when a user navigates
    # away from an edit screen that's been open for very long.
    # When this happens, LockableModel.unlock_for will throw an exception, 
    # and we just ignore the request.
    # That way, any new lock that may since have been put in place by another 
    # user won't get accidentally overwritten.
    try:
        obj = Lock.objects.get(entry_id=id, app=app, model=model)
        obj.delete()

        return HttpResponse(status=200)
    except:
        return HttpResponse(status=403)

@log
@user_may_change_model
@is_lockable
def is_locked(request, app, model, id):
    data = {'is_active': False,
            'applies': False,
            'for_user': None}
    try:
        obj = Lock.objects.get(entry_id=id, app=app, model=model)    
    except Lock.DoesNotExist:
        pass
    else:
        data['is_active']  = obj.is_locked
        data['for_user']  = getattr(obj.locked_by, 'username', None)
        data['applies']  = obj.lock_applies_to(request.user)

    response = simplejson.dumps(data)
    return HttpResponse(response, mimetype='application/json')
@log
def js_variables(request):
    response = "var locking = " + simplejson.dumps({
        'base_url': "/".join(request.path.split('/')[:-1]),
        'timeout': LOCK_TIMEOUT,
        'time_until_expiration': settings.LOCKING['time_until_expiration'],
        'time_until_warning': settings.LOCKING['time_until_warning'],
        'admin_url': "/".join(_s.LOCKING_URL.split('/')[:-1]),
    })

    return HttpResponse(response, mimetype='application/json')

