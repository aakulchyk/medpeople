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
    class Meta:
        ordering = ['pk']

    COMMON_RECIPE = 0
    COMMON_DIAGNOSIS = 1
    COMMON_ANALYSIS_TABLE = 2
    SYNEVO_ANALYSIS_TABLE = 3

    DOCUMENT_TYPE_CHOICES = (
        (COMMON_RECIPE, "Common Recipe"),
        (COMMON_DIAGNOSIS, "Common Diagnosis"),
        (COMMON_ANALYSIS_TABLE, "Common Analysis Table"),
        (SYNEVO_ANALYSIS_TABLE, "Synevo Analysis Table"),
    )

    type = models.IntegerField(
        choices = DOCUMENT_TYPE_CHOICES,
        default = COMMON_RECIPE,
    )

    def __str__(self):
        return self.type

    def isTable(self):
        return self.type in (self.COMMON_ANALYSIS_TABLE,
                             self.SYNEVO_ANALYSIS_TABLE)
