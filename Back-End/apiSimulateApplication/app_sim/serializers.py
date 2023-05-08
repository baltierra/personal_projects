from rest_framework import serializers
from app_sim.models import WeightedCareer

class WeightedCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightedCareer 
        fields = ('weighted_career_id', 'demre_code', 'weighted_threshold',
                  'unique_code', 'nem_weight', 'ranking_weight', 'math_weight',
                  'lang_weight', 'hist_weight', 'scie_weight', 'other_weight')