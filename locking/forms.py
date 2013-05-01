from django import forms
from django.contrib.contenttypes.models import ContentType

from locking.models import Lock


class LockingForm(forms.ModelForm):
    """
    Clean the form to enforce orm locking before saving the object.  This will
    only work if you set lock_type to 'hard' in the locking.models file.
    """

    def clean(self):
        self.cleaned_data = super(LockingForm, self).clean()
        try:
            content_type = ContentType.objects.get_for_model(self.obj)
            lock = Lock.objects.get(entry_id=self.obj.id, app=content_type.app_label, model=content_type.model)
        except:
            return self.cleaned_data
        if lock.is_locked:
            if lock.locked_by != self.request.user and lock.lock_type == 'hard':
                mins_remaining = int(round(lock.lock_seconds_remaining / 60))
                raise forms.ValidationError((
                    "You cannot save this object because it is locked by user"
                    " %(user)s for roughly %(mins_remaining)s more "
                    "minute%(s)s.") % {
                        'user': lock.locked_by.username,
                        'mins_remaining': mins_remaining,
                        's': '' if mins_remaining == 1 else 's',
                    })
        return self.cleaned_data
