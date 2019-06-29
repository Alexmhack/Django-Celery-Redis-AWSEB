from __future__ import absolute_import, unicode_literals

from celery import shared_task

from samples.models import Sample

@shared_task
def add(x, y):
	try:
		x = int(x)
		y = int(y)
		value = (x + y)
		Sample.objects.create(value=value)
	except Exception as e:
		pass
