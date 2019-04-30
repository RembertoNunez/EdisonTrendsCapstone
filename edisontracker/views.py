from django.shortcuts import render
from django.http import JsonResponse
import os
import random
import folium
from uszipcode import SearchEngine
import pandas as pd
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy as scipy
import datetime

def home(request):
    catagories = {"Electronics": ["Amazon", "Best Buy"],
                  "Food Delivery": ["Grub Hub", "Door Dash", "Instacart"],
                  "Apparel": ["Ralph Lauren", "Nordstrom", "H&M", "Hot Topic", "Gap"],
                  "Footwear": ["Adidas", "Nike"],
                  "Sportswear": ["Nike", "Adidas", "Under Armour"],
                  "Retail (General)": ["Amazon", "Kmart", "Target", "Walmart", "Costco"],
                  "Grocery": ["Publix", "Whole Foods Market", "Safeway"],
                  "Fast Food": ["Pizza Hut", "Domino's Pizza", "Panda Express"],
                  "Pizza": ["Pizza Hut", "Domino's Pizza", "Papa John's"]}
    return render(request, 'edisontracker/index.html', {"categories": catagories})


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

    html = render(request, 'edisontracker/map.html', {"map": map_html})

    return html

def marketsale(request):
    dat = pd.read_csv('edisontracker/static/edisontracker/csv/anonymous_sample.csv')

    catagories = {"Electronics": ["Amazon", "Best Buy"], "Food Delivery": ["Grub Hub", "Door Dash", "Instacart"],
                  "Apparel": ["Ralph Lauren", "Nordstrom", "H&M", "Hot Topic", "Gap"], "Footwear": ["Adidas", "Nike"],
                  "Sportswear": ["Nike", "Adidas", "Under Armour"],
                  "Retail (General)": ["Amazon", "Kmart", "Target", "Walmart", "Costco"],
                  "Grocery": ["Publix", "Whole Foods Market", "Safeway"],
                  "Fast Food": ["Pizza Hut", "Domino's Pizza", "Panda Express"],
                  "Pizza": ["Pizza Hut", "Domino's Pizza", "Papa John's"]}

    merchants = ["Merchant 1", "Merchant 2", "Merchant 3"]
    xlab = None
    tick = 5
    trend = False
    rval = False
    # On_load
    year_week = []
    for date in np.array(dat["email_day"]):
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        week = datetime.date(int(year), int(month), int(day)).isocalendar()[1]
        text = str(year) + "-" + "{:02d}".format(week)
        year_week.append(text)
    dat["week"] = year_week

    sales = pd.DataFrame()
    all_weeks = dat["week"].unique()
    all_weeks.sort()
    for week in all_weeks:
        sales = sales.append(dat.loc[dat["week"] == week, "merchant_name"].value_counts(), ignore_index=True)

    compare = sales[merchants]
    compare.plot(title="Sales Across a Time Range")
    plt.xticks(np.arange(len(all_weeks), step=5), all_weeks[0::5], rotation=-75)
    plt.xlabel("Time Range")
    plt.ylabel("Number of Sales Records")
    plt.tight_layout()
    plt.savefig('edisontracker/static/edisontracker/plot/plot1.png')
    plt.close()

    compare = compare.assign(x=np.array(range(compare.shape[0])))
    market_share_plot(compare, all_weeks, trend=True, rval=False)

    html = render(request, 'edisontracker/marketsales.html',  {"company_list": catagories})

    return html

def market_share_plot(dat, xlab = None, tick=5, trend=False, rval=False):
    if xlab is not None:
        if dat.shape[0] is not len(xlab):
            print("Error: xlab length does not match the data")
            print(str(dat.shape[0]) + " != " + str(len(xlab)))

    dat = pd.DataFrame(dat)
    num_companies = dat.shape[1] - 1

    # Creates a list of companies
    company_names = []
    for column_name in dat.columns:
        if column_name is not "x":
            company_names.append(column_name)

    # Calculates the probabilities
    probs = pd.DataFrame()
    comp = 0
    for company in company_names:
        start = dat[company][0] / (dat.loc[0, dat.columns != 'x'].sum())
        prob_row = []

        # Finds the percentage for each value, minus the first value of the company
        for row in range(len(dat[company])):
            prob = ((dat[company][row] / (dat.loc[row, dat.columns != 'x'].sum())) - start) * 100
            if pd.isna(prob) or prob == None:
                if pd.isna(start):
                    prob = 0
                else:
                    prob = 0 - start
            prob_row.append(prob)

        # Adds the probabilities to a new column in the dataframe
        probs = probs.assign(c=pd.Series(prob_row))
        probs = probs.rename(columns={'c': company_names[comp]})
        comp += 1

    # Plots the probabilities over time
    probs.plot()
    plt.xlabel("Time Range")
    plt.ylabel("% Change")
    plt.title("Change in Market Share Over Time")
    plt.axhline(y=0, color="gray", linewidth=1, linestyle="--")

    # Add the x label text if given
    if xlab is not None:
        plt.xticks(np.arange(len(xlab), step=tick), xlab[0::tick], rotation=-75)

    # Add the trend lines
    plt.gca().set_prop_cycle(None)
    if trend:
        r_values = {}
        xrange = np.arange(0, probs.shape[0], 1)
        i = 0
        for p in probs:

            # Calculate and plot the equation of the trend line for each company
            slope, intercept, r, p, error = scipy.stats.linregress(xrange, probs[p])
            if rval:
                r_values[probs.columns[i]] = r

            line = slope * xrange + intercept
            plt.plot(xrange, line, linestyle="--", linewidth=1)
            i += 1
    plt.tight_layout()
    plt.savefig('edisontracker/static/edisontracker/plot/plot2.png')
    plt.close()
    if trend and rval:
        return r_values
