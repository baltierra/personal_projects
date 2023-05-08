from django.db import models

# Create your models here.
class WeightedCareer(models.Model):
    weighted_career_id = models.AutoField(primary_key=True)
    demre_code = models.CharField(max_length=15)
    weighted_threshold = models.FloatField()
    unique_code = models.CharField(max_length=15)
    nem_weight = models.PositiveSmallIntegerField()
    ranking_weight = models.PositiveSmallIntegerField()
    math_weight = models.PositiveSmallIntegerField()
    lang_weight = models.PositiveSmallIntegerField()
    hist_weight = models.PositiveSmallIntegerField()
    scie_weight = models.PositiveSmallIntegerField()
    other_weight = models.PositiveSmallIntegerField()
    

# class SimulatedApplication(models.Model):
#     simulation_id = models.AutoField(primary_key=True)
#     applicant_id = models.CharField(max_length=10)
#     nem_score = models.PositiveSmallIntegerField()
#     predicted_ranking = models.PositiveSmallIntegerField()
#     math_score = models.PositiveSmallIntegerField()
#     lang_score = models.PositiveSmallIntegerField()
#     hist_score = models.PositiveSmallIntegerField()
#     scie_score = models.PositiveSmallIntegerField()
#     major_unique_code = models.CharField(max_length=15)
#     simulated_score = models.FloatField()
#     simulation_result = models.BooleanField()
#     simulation_date = models.DateField()