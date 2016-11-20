from django.db import models


class MedicalTerm(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    weight = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    @classmethod
    def objectsByNames(cls, filter_names):
        filters = []
        for f in filter_names:
            for found in cls.objects.filter(name=f):
                filters.append(found)
        if not filters:
            filters.append(MedicalTerm())
        return filters


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
