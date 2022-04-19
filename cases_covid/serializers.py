from rest_framework import serializers
from cases_covid import models

class CovidSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = models.cases_Ecuador_covid
        fields = ['fecha','total_casos']