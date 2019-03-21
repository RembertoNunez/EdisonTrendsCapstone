from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    companyList = ["Burger King", "Jack in the Box", "McDonald", "Taco Bell", "Chipotle Burrito Bar", " Chick-Fil-A", "Wendy's"]
    companyList.sort()
    return render(request, 'edisontracker/index.html', {"company_list": companyList})
