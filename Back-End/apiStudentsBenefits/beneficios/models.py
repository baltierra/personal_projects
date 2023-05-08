from django.db import models

# Create your models here.

class GovBenefits(models.Model):
    ben_id = models.AutoField(primary_key=True)
    ben_name = models.TextField()
    ben_description = models.TextField()
    perc_60 = models.BooleanField()
    perc_70 = models.BooleanField()
    perc_80 = models.BooleanField()
    min_grade = models.FloatField()
    min_score = models.IntegerField()
    reg_or_nat_score = models.BooleanField()
    std_test_req = models.BooleanField()
    top_10_perc_req = models.BooleanField()
    academic_progression_req = models.BooleanField()
    tp_only = models.BooleanField()
    requisite_summary = models.TextField()
    additional = models.TextField()