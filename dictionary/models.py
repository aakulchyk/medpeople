from django.db import models


class MedicalTerm(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class BloodType(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name


class DocumentType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
