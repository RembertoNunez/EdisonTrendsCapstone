from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from datetime import date, timedelta
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
from wtforms import StringField
from wtforms.validators import DataRequired
import pandas as pd
import matplotlib.pyplot as plt
import math

import json



search = SearchEngine(simple_zipcode = True)

dat = pd.read_csv('edisontracker/static/edisontracker/csv/anonymous_sample.csv')
state_zip = {}

def home(request):
    categories = {"Electronics": ["Amazon", "Best Buy"], "Food Delivery": ["Grub Hub", "Door Dash", "Instacart"],
                  "Apparel": ["Ralph Lauren", "Nordstrom", "H&M", "Hot Topic", "Gap"], "Footwear": ["Adidas", "Nike"],
                  "Sportswear": ["Nike", "Adidas", "Under Armour"],
                  "Retail (General)": ["Amazon", "Kmart", "Target", "Walmart", "Costco"],
                  "Grocery": ["Publix", "Whole Foods Market", "Safeway"],
                  "Fast Food": ["Pizza Hut", "Domino's Pizza", "Panda Express"],
                  "Pizza": ["Pizza Hut", "Domino's Pizza", "Papa John's"]}

    return render(request, 'edisontracker/index.html', {"categories": categories})

def getOptions(request):
    choice = request.GET.get("choice")
    merchants = ["Amazon", "Best Buy", "Grub Hub", "Door Dash", "Instacart",
                  "Ralph Lauren", "Nordstrom", "H&M", "Hot Topic", "Gap","Adidas", "Nike",
                  "Nike", "Adidas", "Under Armour",
                  "Amazon", "Kmart", "Target", "Walmart", "Costco",
                  "Publix", "Whole Foods Market", "Safeway",
                  "Pizza Hut", "Domino's Pizza", "Panda Express",
                  "Pizza Hut", "Domino's Pizza", "Papa John's"]
    merchants.remove(choice)
    display = ""
    for merchant in merchants:
        display += "<div class ='form-check form-check-inline' style= 'width: 500px'>"
        display += "<input class ='form-check-input' type='checkbox' name='merchants' value=\"" + merchant + "\" id='merchants'>"
        display += "<label class ='form-check-label' for ='merchants' >" + merchant + "</label> </div>"
    html = HttpResponse(display)
    return html

# run with command: FLASK_APP=app.py; flask run
def salesHome(request):
    catagories = {"Electronics": ["Merchant 1", "Merchant 6"],
                  "Food Delivery": ["Merchant 5", "Merchant 10", "Merchant 4"],
                  "Apparel": ["Merchant 23", "Merchant 9", "Merchant 16", "Merchant 21", "Merchant 15"],
                  "Footwear": ["Merchant 22", "Merchant 17"],
                  "Sportswear": ["Merchant 17", "Merchant 22", "Merchant 20"],
                  "Retail (General)": ["Merchant 1", "Merchant 12", "Merchant 8", "Merchant 2", "Merchant 13"],
                  "Grocery": ["Merchant 13", "Merchant 24", "Merchant 14"],
                  "Fast Food": ["Merchant 7", "Merchant 3", "Merchant 19"],
                  "Pizza": ["Merchant 7", "Merchant 3", "Merchant 11"]}
    return render(request, 'edisontracker/marketsales.html', {"categories": catagories})

def allSaleHome(request):
    catagories = {"Electronics": ["Merchant 1", "Merchant 6"],
                  "Food Delivery": ["Merchant 5", "Merchant 10", "Merchant 4"],
                  "Apparel": ["Merchant 23", "Merchant 9", "Merchant 16", "Merchant 21", "Merchant 15"],
                  "Footwear": ["Merchant 22", "Merchant 17"],
                  "Sportswear": ["Merchant 17", "Merchant 22", "Merchant 20"],
                  "Retail (General)": ["Merchant 1", "Merchant 12", "Merchant 8", "Merchant 2", "Merchant 13"],
                  "Grocery": ["Merchant 13", "Merchant 24", "Merchant 14"],
                  "Fast Food": ["Merchant 7", "Merchant 3", "Merchant 19"],
                  "Pizza": ["Merchant 7", "Merchant 3", "Merchant 11"]}

    html = render(request, 'edisontracker/salescompany.html', {"categories": catagories})

    return html

def mapGenerate(request):
    search = SearchEngine(simple_zipcode=True)

    data = pd.read_csv('edisontracker/static/edisontracker/csv/anonymous_sample.csv')

    to_plot = request.GET.get("to_plot")
    compare = request.GET.getlist("compare[]")

    compare.append(to_plot)

    map_obj = plot_market_on_map(data, compare, to_plot)

    style_statement = '<style>.leaflet-control{color:#00FF00}</style>'
    map_obj.get_root().html.add_child(folium.Element(style_statement))
    map_html = map_obj.get_root().render()
    filename = "map"
    file = open("edisontracker/static/edisontracker/plot/" + filename + ".html", "w")
    file.write(map_html)
    file.close()

    html = HttpResponse(
        "")

    return html

def getMap(request):
    html = render(request, 'edisontracker/map.html')

    return html

def plot_market_on_map(data, compare, to_plot):


    dat_state = data.loc[:, ['user_zip_code', 'merchant_name', 'email_day']]
    dat_state = dat_state.loc[dat_state['merchant_name'].isin(compare), :]

    # Add the state column
    dat_state['state'] = dat_state['user_zip_code'].apply(lambda x: find_state(x))

    year_week = []
    day_to_week = {}
    for date in np.array(dat_state["email_day"]):
        if date in day_to_week.keys():
            year_week.append(day_to_week[date])
        else:
            year = date[0:4]
            month = date[5:7]
            day = date[8:10]
            week = datetime.date(int(year), int(month), int(day)).isocalendar()[1]
            text = str(year) + "-" + "{:02d}".format(week)
            year_week.append(text)
    dat_state["week"] = year_week

    grouped_state = dat_state.groupby('state')

    np.seterr(all="ignore")

    state_change = pd.DataFrame(columns=['State', 'Change'])
    row_to_add = 0

    for state in grouped_state:

        sales = pd.DataFrame()
        all_weeks = dat_state["week"].unique()
        all_weeks.sort()
        for week in all_weeks:
            sale_count = state[1].loc[state[1]["week"] == week, "merchant_name"].value_counts()
            sales = sales.append(sale_count, ignore_index=True)

        compare = sales.fillna(0)
        compare = compare.assign(x=np.array(range(compare.shape[0])))


        res = market_share_change(compare)


        if to_plot in list(res.keys()):
            state_change.loc[row_to_add] = [state[0], res[to_plot]]

        else:
            state_change.loc[row_to_add] = [state[0], 0]

        row_to_add += 1

    state_edges = os.path.join('edisontracker/static/edisontracker/csv/states.geojson')

    map_obj = folium.Map(
        location=[39.8283, -98.5795],
        zoom_start=4,
        tiles='OpenStreetMap'
    )

    minimum = min(state_change["Change"])
    maximum = max(state_change["Change"])
    breaks = 5
    limit = max(abs(math.floor(minimum)), abs(math.ceil(maximum)))
    scale = list(np.histogram(np.arange(math.floor((-limit) / breaks) * breaks, 0 + 1), bins=breaks)[1])
    scale.extend(list(np.histogram(np.arange(0, math.ceil((limit) / breaks) * breaks + 1), bins=breaks)[1]))
    folium.Choropleth(
        geo_data=state_edges,
        data=state_change,
        columns=["State", "Change"],
        key_on='feature.properties.name',
        fill_color='RdYlBu',
        fill_opacity=0.8,
        line_opacity=0.6,
        threshold_scale=scale,
        reset=True

    ).add_to(map_obj)

    return map_obj


def market_share_change(dat):
    import sys

    # Creates a list of companies
    company_names = []
    for column_name in dat.columns:
        if column_name is not "x":
            company_names.append(column_name)

    # Calculates the probabilities
    probs = pd.DataFrame()
    comp = 0
    for company in company_names:
        denom = dat.loc[0, dat.columns != 'x'].sum()
        if denom != 0:
            start = dat[company][0] / denom
        else:
            start = 1 / len(company_names)
        prob_row = []

        # Finds the percentage for each value, minus the first value of the company
        for row in range(len(dat[company])):
            denom = dat.loc[row, dat.columns != 'x'].sum()
            if denom != 0:
                prob = ((dat[company][row] / denom) - start) * 100
            else:
                prob = 0
            prob_row.append(prob)

        # Adds the probabilities to a new column in the dataframe
        probs = probs.assign(c=pd.Series(prob_row))
        probs = probs.rename(columns={'c': company_names[comp]})
        comp += 1

    max_x = probs.shape[0] - 1
    xrange = np.arange(0, probs.shape[0], 1)

    changes = {}
    for company in probs:
        slope, intercept, r, p, error = scipy.stats.linregress(xrange, probs[company])
        changes[company] = slope * max_x

    return changes

def find_state(zip):
    state = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'Washington DC': 'DC',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}
    get_full = {v: k for k, v in state.items()}

    if zip in state_zip:
        return state_zip[zip]
    else:
        state_abrv = search.by_zipcode(str(zip)).state
        if state_abrv is not None:
            state = get_full[state_abrv]
            state_zip[zip] = state
            return state

def marketsale(request):
    dat = pd.read_csv('edisontracker/static/edisontracker/csv/anonymous_sample.csv')

    # catagories = {"Electronics": ["Merchant 1", "Merchant 6"],
    #               "Food Delivery": ["Merchant 5", "Merchant 10", "Merchant 4"],
    #               "Apparel": ["Merchant 23", "Merchant 9", "Merchant 16", "Merchant 21", "Merchant 15"],
    #               "Footwear": ["Merchant 22", "Merchant 17"],
    #               "Sportswear": ["Merchant 17", "Merchant 22", "Merchant 20"],
    #               "Retail (General)": ["Merchant 1", "Merchant 12", "Merchant 8", "Merchant 2", "Merchant 13"],
    #               "Grocery": ["Merchant 13", "Merchant 24", "Merchant 14"],
    #               "Fast Food": ["Merchant 7", "Merchant 3", "Merchant 19"],
    #               "Pizza": ["Merchant 7", "Merchant 3", "Merchant 11"]}
    #
    # merchantType = request.GET.get("category")
    # start_date = request.GET.get("start_date")
    # end_date = request.GET.get("end_date")
    # merchants = []
    #
    # for item in catagories[merchantType]:
    #     merchants.append(item)
    # print(merchants)
    # print(start_date)
    # print(end_date)

    # merchantType = []
    # merchantType.append(request.GET.get("merchantChoice"))
    merchantType = request.GET.get("merchantChoice")
    merchants = json.loads(merchantType)
    print(merchants)

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
    plt.savefig('edisontracker/static/edisontracker/plot/plotTimeSale.png')
    plt.close()

    compare = compare.assign(x=np.array(range(compare.shape[0])))
    market_share_plot(compare, all_weeks, trend=True, rval=False)

    html = HttpResponse('{ "plotTimeSale" : "/static/edisontracker/plot/plotTimeSale.png", "plotMarketShare" : "/static/edisontracker/plot/plotMarketShare.png" }')

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
    plt.savefig('edisontracker/static/edisontracker/plot/plotMarketShare.png')
    plt.close()
    if trend and rval:
        return r_values


def allSales(request):
    global dat
    image_path = 'edisontracker/static/edisontracker/plot/plotAllSales.png'
    plt.figure(1)
    dat["merchant_name"].value_counts().plot(kind="bar", color="red")
    plt.title("Sales per Company")
    plt.show()
    plt.savefig(image_path, bbox_inches="tight")
    plt.close()

    html = HttpResponse('{"plotAllSales" : "/static/edisontracker/plot/plotAllSales.png"}')

    return html

def loadBarPlotNumSales(request):
    global dat
    year_month = []
    try:
        dat["month"]
    except KeyError:
        for date in np.array(dat["email_day"]):
            year_month.append(date[0:7])
        dat["month"] = year_month
    # convert to datetime objects
    dat["email_day"] = pd.to_datetime(dat["email_day"])

   #html = render('initial.html', select=build_options())
    html = render(request, 'edisontracker/barplotNumSales.html', {"select": build_options()})
    return html

def build_options(feat = None ):
    global dat
    merchants = sorted(list(dat.merchant_name.unique()))
    options = "<select id = 'merchant' class='custom-select my-1 mr-sm-2 mb-3' form=\"form\", name=\"feat\">"
    for merchant in merchants:
        if merchant == feat:
            options += "<option class='custom-select my-1 mr-sm-2 mb-3' value=\"" + merchant + \
                       "\" selected>" + merchant + "</option>"
        else:
            options += "<option class='custom-select my-1 mr-sm-2 mb-3' value=\"" + merchant + "\">" + merchant + "</option>"
    options += "<select>"
    return options

def getMerchants(request):
    catagories = {"Electronics": ["Amazon", "Best Buy"], "Food Delivery": ["Grub Hub", "Door Dash", "Instacart"],
                  "Apparel": ["Ralph Lauren", "Nordstrom", "H&M", "Hot Topic", "Gap"], "Footwear": ["Adidas", "Nike"],
                  "Sportswear": ["Nike", "Adidas", "Under Armour"],
                  "Retail (General)": ["Amazon", "Kmart", "Target", "Walmart", "Costco"],
                  "Grocery": ["Publix", "Whole Foods Market", "Safeway"],
                  "Fast Food": ["Pizza Hut", "Domino's Pizza", "Panda Express"],
                  "Pizza": ["Pizza Hut", "Domino's Pizza", "Papa John's"]}

    merchantType = request.GET.get("category")
    merchants = []
    for item in catagories[merchantType]:
        merchants.append(item)

    display = ""

    for merchant in merchants:
        display += "<div class ='form-check form-check-inline'>"
        display += "<input class ='form-check-input' type='checkbox' name='merchants' value=\"" + merchant + "\" id='merchants'>"
        display += "<label class ='form-check-label' for ='merchants' >" + merchant + "</label> </div>"
    html = HttpResponse(display)
    return html

def getBarPlot(request):
    feat = request.GET.get("feat")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    title = "Sales per Month for %s from %s to %s" % (feat, start_date, end_date)
    # "first string is: %s, second one is: %s" % (str1, "geo.tif")
    print(start_date)
    print(end_date)
    # create the plot
    image_path = 'edisontracker/static/edisontracker/plot/plotMarketShare.png'
    selected = (dat["merchant_name"] == feat) & (
            dat["email_day"] >= start_date) & (dat["email_day"] <= end_date)
    df = dat.loc[selected]
    plt.figure(1)
    df["month"].value_counts().sort_index().plot(kind="bar", color="red")
    plt.grid(color='gray', linestyle='-', linewidth=1)

    plt.title(title)
    plt.savefig(image_path)
    plt.close()

    html = HttpResponse('{"plot" : "/static/edisontracker/plot/plotMarketShare.png"}')

    return html
