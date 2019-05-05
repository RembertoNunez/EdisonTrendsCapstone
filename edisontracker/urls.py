from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tracker-edisontracker'),
    path('map', views.mapGenerate, name='tracker-edisontracker'),
    path('index.html', views.home, name='tracker-edisontracker'),
    path('marketSales.html', views.salesHome, name='tracker-edisontracker'),
    path('getPlot', views.marketsale, name='tracker-edisontracker'),
    path('salesCompany.html', views.allSaleHome, name='tracker-edisontracker'),
    path('getSalePlot', views.allSales, name='tracker-edisontracker'),
    path('barPlot.html', views.loadBarPlotNumSales, name='tracker-edisontracker'),
    path('getBarPlot', views.getBarPlot, name='tracker-edisontracker'),

]
