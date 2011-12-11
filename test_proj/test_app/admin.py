from django.contrib import admin
from locking.admin import LockableAdmin
from test_proj.test_app.models import TestModel

class TestModelAdmin(LockableAdmin):
    pass
admin.site.register(TestModel, TestModelAdmin)
