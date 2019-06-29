from __future__ import absolute_import, unicode_literals

from celery import shared_task

from samples.models import Sample

@shared_task
def add(x, y):
	x = int(x)
	y = int(y)
	value = (x + y)
	s = Sample.objects.create(value=value)
	return s
