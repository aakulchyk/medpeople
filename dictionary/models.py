from django.db import models


class MedicalTerm(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	def __str__(self):
		return self.name
