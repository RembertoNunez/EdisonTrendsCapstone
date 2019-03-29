from django.shortcuts import render
from django.http import JsonResponse
import os
import random
import folium
from uszipcode import SearchEngine

def home(request):
    companyList = ["Burger King", "Jack in the Box", "McDonald", "Taco Bell", "Chipotle Burrito Bar", " Chick-Fil-A", "Wendy's"]
    companyList.sort()
    return render(request, 'edisontracker/index.html', {"company_list": companyList})


# run with command: FLASK_APP=app.py; flask run


def mapGenerate(request):
    search = SearchEngine(simple_zipcode=True)

    # app = Flask(__name__, static_url_path='/static')

    zips = [
        "10468", "91710", "34759", "55410", "20164", "30044", "38663",
        "72916", "28411", "98116", "67230", "33496", "19064", "78130",
        "90403", "90290", "46013", "94114", "95361", "91754", "41076",
        "38002", "38017", "10011", "34759", "42701", "19053", "89521",
        "85749", "16855", "18037", "98056", "34787", "08520", "75009",
        "84780", "33897", "52060", "89166", "85302", "91604", "27526",
        "92253", "19050", "07075", "43017", "11102", "33321", "71111",
        "19610", "75114", "92054", "53511", "95348", "63304", "60193",
        "42701", "13642", "77845", "30238", "95020"]

    map_obj = folium.Map(
        location=[39.8283, -98.5795],
        zoom_start=4,
        tiles='OpenStreetMap'
    )

    for code in zips:
        zip_info = search.by_zipcode(code)
        coord = zip_info.lat, zip_info.lng
        icon = folium.features.CustomIcon('edisontracker/static/edisontracker/images/red_circle.png', icon_size=(10, 10))
        folium.Marker(coord, icon=icon).add_to(map_obj)

    style_statement = '<style>.leaflet-control{color:#00FF00}</style>'
    map_obj.get_root().html.add_child(folium.Element(style_statement))
    map_html = map_obj.get_root().render()

    filename = str(random.randint(1, 9999999999))
    file = open("edisontracker/static/edisontracker/"+filename + ".html", "w")
    file.write(map_html)
    file.close()
    html = render(request, 'edisontracker/map.html', {"filename": filename})

    return html
