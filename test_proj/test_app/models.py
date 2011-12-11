from django.db import models
from locking.models import LockableModel

class TestModel(LockableModel):
	title = models.CharField(max_length=80)
	content = models.TextField()
