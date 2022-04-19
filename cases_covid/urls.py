from cases_covid import views
from django.urls import path

urlpatterns = [
    path('', views.CovidApiView.as_view())
]