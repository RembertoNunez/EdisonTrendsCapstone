
categories = {"Electronics": ["Amazon", "Best Buy"], "Food Delivery": ["Grub Hub", "Door Dash", "Instacart"],
                  "Apparel": ["Ralph Lauren", "Nordstrom", "H&M", "Hot Topic", "Gap"], "Footwear": ["Adidas", "Nike"],
                  "Sportswear": ["Nike", "Adidas", "Under Armour"],
                  "Retail (General)": ["Amazon", "Kmart", "Target", "Walmart", "Costco"],
                  "Grocery": ["Publix", "Whole Foods Market", "Safeway"],
                  "Fast Food": ["Pizza Hut", "Domino's Pizza", "Panda Express"],
                  "Pizza": ["Pizza Hut", "Domino's Pizza", "Papa John's"]}

merchants = ["Amazon", "Best Buy", "Grub Hub", "Door Dash", "Instacart",
                  "Ralph Lauren", "Nordstrom", "H&M", "Hot Topic", "Gap","Adidas", "Nike",
                  "Nike", "Adidas", "Under Armour", "Kmart", "Target",
                  "Walmart", "Costco", "Publix", "Whole Foods Market", "Safeway",
                  "Pizza Hut", "Domino's Pizza", "Panda Express", "Papa John's"]
state_zip = {}

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
