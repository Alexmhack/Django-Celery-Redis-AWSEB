from django.db import models

class Sample(models.Model):
	value = models.PositiveIntegerField()

	def __str__(self):
		return str(self.value)
