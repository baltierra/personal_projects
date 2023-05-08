from rest_framework import serializers
from beneficios.models import GovBenefits

class BenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovBenefits 
        fields = ('ben_id','ben_name','ben_description','perc_60','perc_70',
                  'perc_80', 'min_grade', 'min_score', 'reg_or_nat_score',
                  'std_test_req', 'top_10_perc_req', 'academic_progression_req',
                  'tp_only', 'requisite_summary', 'additional')