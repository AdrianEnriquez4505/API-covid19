from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests as rq

from cases_covid import serializers
from cases_covid import models

from datetime import datetime
# Create your views here.

class CovidApiView(APIView):

    serializer_class = serializers.CovidSerializer
    queryset = models.cases_Ecuador_covid.objects.all()

    def get(self, request, format=None):
        data = models.cases_Ecuador_covid.objects.values()
        data1=[]
        for i in data:
            serializer = serializers.CovidSerializer(data=i)
            if serializer.is_valid():
                data1.append(serializer.data)

        return Response(data1, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        try:
            url = 'https://api.covid19api.com/dayone/country/ecuador/status/confirmed'
            data = rq.get(url)
            data1 = data.json()

            data_crear={'fecha':data1[-1]['Date'], 'total_casos':data1[-1]['Cases']}
            fecha_crear = datetime.strptime(data_crear['fecha'],'%Y-%m-%dT%H:%M:%SZ')

            qs = list(models.cases_Ecuador_covid.objects.all())
            year_base, year_crear = (qs[-1].fecha.year,fecha_crear.year)
            month_base, month_crear = (qs[-1].fecha.month, fecha_crear.month)
            day_base, day_crear = (qs[-1].fecha.day, fecha_crear.day)

            if (year_base!=year_crear) or (month_base!=month_crear) or (day_base!=day_crear):
                cases_covid = models.cases_Ecuador_covid(fecha=data_crear['fecha'], total_casos=data_crear['total_casos'])
                cases_covid.save()

                return Response({'message':'Caso creado con éxito'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message':'Caso no creado, pues el caso ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message':'Caso no creado'}, status=status.HTTP_400_BAD_REQUEST)
        