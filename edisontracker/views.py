from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    companyList = ["Electronics", "Food Delivery", "Apparel", "Footwear", "Sportswear", "Retail (General)", "Grocery", "Pizza"]
    companyList.sort()
    return render(request, 'edisontracker/index.html', {"company_list": companyList})
