# Import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup, StopParsing 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd
import sys

from urllib3.poolmanager import PoolManager

mel_suburbs = pd.read_csv("Clean_Mel_suburbs.csv")
mel_suburbs = mel_suburbs["suburb"].to_list()
mel_suburbs = list(set(mel_suburbs))
mel_suburbs.sort()
mel_suburbs = mel_suburbs[350:500]

# Get suburbs and postcodes of Melbourne city
def get_suburb(suburbs):
    vic_suburbs = ["vic/" + suburb for suburb in suburbs]
    return vic_suburbs

# Manipulate the search
# default: search any results
# advanced: search any results with filter conditions
search = str(input("Enter search (default, advanced): "))

# Get url
def get_url():
    pages = []

    # search constraint
    if not search in ["default", "advanced"]:
        return "Invalid search"

    elif search == "default":
        for suburb in get_suburb(mel_suburbs):
            page = "https://www.onthehouse.com.au/real-estate/" + suburb + "?" + "page="
            pages.append(page)

    elif search == "advanced":
        # bed constraints
        min_bed_no = str(input("Enter the minimum number of beds(Any, 1-5): "))
        min_bed = str("bedsMin=" + min_bed_no + "&")
        if min_bed_no == "Any":
            min_bed = re.sub(min_bed, "", min_bed)
        elif not min_bed_no in ["Any", "1", "2", "3", "4", "5"] or len(min_bed) != 10:
            return print("Invalid number of minimum beds")
        max_bed_no = str(input("Enter the maxium number of beds (Any, 1-5): "))
        max_bed = str("bedsMax=" + max_bed_no + "&")
        if max_bed_no == "Any":
            max_bed = re.sub(max_bed, "", max_bed)
        elif not max_bed_no in ["Any", "1", "2", "3", "4", "5"] or len(max_bed) != 10:
            return print("Invalid number of maximum beds")
        else:
            if min_bed_no != "Any" and int(min_bed_no) >= int(max_bed_no):
                return print("The minimum beds are not smaller than the maximum beds")
         
        # price constraints
        min_property_price = str(input("Enter the minimum price (Any, 50000 - 15000000000): "))
        min_price = str("priceMin=" + str(min_property_price) + "&")
        if min_property_price == "Any":
            min_price = re.sub(min_price, "", min_price)
        else:
            try:
                min_property_price = int(min_property_price)
            except ValueError:
                return print("Invalid minimum property price")
            else:
                if int(min_property_price) < 50000 or int(min_property_price) > 15000000000:
                    return print("Invalid minimum property price")
        max_property_price = str(input("Enter the maximum price (Any, 50000 - 15000000000): "))
        max_price = str("priceMax=" + str(max_property_price) + "&")
        if max_property_price == "Any":
            max_price = re.sub(max_price, "", max_price)
        else:
            try:
                max_property_price = int(max_property_price)
            except ValueError:
                return print("Invaliid maximum property price")
            else:
                if int(max_property_price) < 5000 or int(max_property_price) > 15000000000:
                    return print("Invalid maximum property price")
                elif min_property_price != "Any" and int(min_property_price) >= int(max_property_price):
                    return print("The minimum price is not smaller than the maximum price")

        # bathroom constraints
        min_bath_no = str(input("Enter the minimum number of bathrooms (Any, 1-5): "))
        min_bath = str("bathsMin=" + min_bath_no + "&")
        if min_bath_no == "Any":
            min_bath = re.sub(min_bath, "", min_bath)
        elif not min_bath_no in ["Any", "1", "2", "3", "4", "5"] or len(min_bath) != 11:
            return print("Invalid minimum number of bathrooms")
        max_bath_no = str(input("Enter the maximum number of bathrooms (Any, 1-5): "))
        max_bath = str("bathsMax=" + max_bath_no + "&")
        if max_bath_no == "Any":
            max_bath = re.sub(max_bath, "", max_bath)
        elif not max_bath_no in ["Any", "1", "2", "3", "4", "5"] or len(max_bath) != 11:
            return print("Invalid maximum number of bathrooms")
        else:
            if min_bath_no != "Any" and int(min_bath_no) >= int(max_bath_no):
                return print("The minimum number of bathrooms are not smaller than the maximum number of bathrooms")

        # car constraints
        min_car_no = str(input("Enter the minimum number of car spaces (Any, 1-5): "))
        min_car = str("carSpacesMin=" + min_car_no + "&")
        if min_car_no == "Any":
            min_car = re.sub(min_car, "", min_car)
        elif not min_car_no in ["Any", "1", "2", "3", "4", "5"] or len(min_car) != 15:
            return print("Invalid minimum number of cars") 
        max_car_no = str(input("Enter the maximum number of car spaces (Any, 1-5): "))
        max_car = str("carSpacesMax=" + max_car_no + "&")
        if max_car_no == "Any":
            max_car = re.sub(max_car, "", max_car)
        elif not max_car_no in ["Any", "1", "2", "3", "4", "5"] or len(max_car) != 15:
            return print("Invalid maximum number of cars") 
        else:
            if min_car_no != "Any" and int(min_car_no) >= int(max_car_no):
                return print("The minimum number of cars are not smaller than the maximum number of cars")

        # figure constraints
        figure = str(input("Select a type of property (Any, House, Apartment, Townhouse, Land, Rural): "))
        property_type = str("types=" + figure + "&")
        if figure == "Any":
            property_type = re.sub(property_type, "", property_type)
        elif not figure in ["House", "Apartment", "Townhouse", "Land", "Rural"]:
            return print("Invalid type of property") 
        
        # status constraints
        status = str(input("Enter a status of property or many status of property (off-market, for-sale, for-rent): "))
        property_status = str("status=" + status + "&")
        # if status == "any":
        #     property_status = re.sub(property_status, "", property_status)
        if not status in ["off-market", "for-sale", "for-rent"]:
            return print("Invalid type of status")

        for suburb in get_suburb(mel_suburbs):
            page = "https://www.onthehouse.com.au/real-estate/" + suburb + "?" + min_bed + max_bed + min_price + max_price + min_bath + max_bath + min_car + max_car + property_type + property_status + "page="
            pages.append(page)
    return pages

# Build a function to get html content from each url
def get_soup(url):
    driver = webdriver.Chrome("/Applications/Python 3.8/chromedriver")
    driver.get(url)
    time.sleep(0)
    page = driver.page_source
    driver.quit()
    return BeautifulSoup(page, "html.parser")

# Get soup for each page
def get_html(link):
    soup_list = []
    for i in range(2, 5):
        page = link + str(i)
        soup = get_soup(page)
        if not "We didn't find properties for your search" in str(soup):
            soup_list.append(soup)
        else:
            soup_list.append("")
            break
    return soup_list

soup_list = []
for page in get_url():
    soup_list.append(get_html(page))
soup_list = [soup for soups in soup_list for soup in soups]

# Get content containing url for each page
def get_content():
    url_content = []
    for soup in soup_list:
        if len(soup) != 0:
            url_content.append(soup.find_all("div", {"class" : "PropertySearch__resultSlot--1YH_u"}))
    return url_content

# Get url for each property
def get_url():
    pattern = '''<\/div><a href="(.*?)">'''
    property_url = [url for content in get_content() for url in re.findall(pattern, str(content), re.DOTALL)]
    property_url = ["https://www.onthehouse.com.au" + url for url in property_url]
    url_set = set(property_url)
    property_url = list(url_set)
    return property_url

# Get the html content for each property
def get_html():
    soup_property = [get_soup(url) for url in get_url()]
    return soup_property

soup_property = get_html()

# Build a function to get address
def get_address(pattern):
    address_content = [content.find("h1", {"class" : "m-0 mb-1 mb-md-3 xlText bold600"}) for content in soup_property]
    address = [re.findall(pattern, str(content), re.DOTALL) for content in address_content]
    address = [location if len(location) != 0 else "-" for location in address]
    address = [a_location for location in address for a_location in location]
    return address
# Get street
street_pattern = '''<h1 class="m-0 mb-1 mb-md-3 xlText bold600">(.*?)<div'''
street = get_address(street_pattern)
# Get suburb
suburb_pattern = '''<div class="mt-3 mb-3 mdText">(.*?)<\/div><\/h1>'''''
suburb = get_address(suburb_pattern)

# Build a function to get number of beds, bathrooms, car spaces, floor area
def get_feature(pattern):
    feature_content = [content.find_all("div", {"class" : "d-flex PropertyInfo__propertyAttributes--i9_ay"}) for content in soup_property]
    no_of_features = [re.findall(pattern, str(feature), re.DOTALL) for feature in feature_content]
    no_of_features = [feature if len(feature) != 0 else "-" for feature in no_of_features]
    no_of_features = [a_feature for feature in no_of_features for a_feature in feature]
    return no_of_features
# Get number of beds
bed_pattern = '''div class="icon mr-2 PropertyAttribute__beds--2XT2Y"><\/div><div>(.*?)<\/div><\/div>'''
no_of_bds = get_feature(bed_pattern)
# Get number of baths
bath_pattern = '''<div class="icon mr-2 PropertyAttribute__baths--3KJnv"><\/div><div>(.*?)<\/div><\/div>'''
no_of_baths = get_feature(bath_pattern)
# Get number of car spaces
car_pattern = '''<div class="icon mr-2 PropertyAttribute__carSpaces--3Nj2X"><\/div><div>(.*?)<\/div>'''
no_of_carspaces = get_feature(car_pattern)
# Get floor area
floor_size_pattern = '''<div class="icon mr-2 PropertyAttribute__floorSize--2ZKNM"><\/div><div>(..*?)<span>'''
floor_area = get_feature(floor_size_pattern)
# Get land area
land_size_pattern = '''<div class="icon mr-2 PropertyAttribute__landSize--1Rs7s"><\/div><div>(.*?)<span>'''
land_area = get_feature(land_size_pattern)

# Buid a function to get year built, building type
def get_detail(pattern):
    detail_content = [content.find_all("ul", {"class" : "pl-0 d-flex flex-wrap"}) for content in soup_property]
    property_detail = [detail if len(detail) != 0 else "-" for detail in detail_content]
    property_detail = [re.findall(pattern, str(detail), re.DOTALL) for detail in property_detail]
    property_detail = [detail if len(detail) != 0 else "-" for detail in property_detail]
    property_detail = [a_detail for detail in property_detail for a_detail in detail]
    return property_detail
# Get year built
year_pattern = '''Year Built<\/span><span class="text-secondary w-50">(.*?)<\/span>'''
year_built = get_detail(year_pattern)
# Get building type
type_pattern = '''Building Type<\/span><span class="text-secondary w-50">(..*?)<\/span>'''
building_type = get_detail(type_pattern)

# Build a function to get sold property price, time
def get_history(pattern):
    history_content = [content.find_all("li", {"class" : "d-flex PropertyHistory__eventItem--56jsg"}) for content in soup_property]
    history_content = [str(history) for history in history_content]
    property_history = [re.findall(pattern, str(history), re.DOTALL) for history in history_content]
    property_history = [history if len(history) != 0 else "-" for history in property_history]
    property_history = [", ".join(history) for history in property_history]
    return property_history
# Get sold time
sold_time_pattern = '''div class="text-secondary">(..*?)<\/div>'''
sold_time = get_history(sold_time_pattern)
# Get sold price
sold_price_pattern = '''<div class="bold600 mdText">(.*?)<\/div>'''
sold_price = get_history(sold_price_pattern)

# Get property status
status_soup = [content.find_all("div", {"class" : "d-flex mb-4 align-items-center"}) for content in soup_property]
status_pattern = '''<span class="p-2 pl-5 pr-5 mr-4 smText text-center.*?>(.*?)<\/span>'''
property_status = [re.findall(status_pattern, str(soup), re.DOTALL) for soup in status_soup]
property_status = [i if len(i) != 0 else "-" for i in property_status]
property_status = [a for b in property_status for a in b]

# Build a function to get listing price
def get_price(re_status):
    if len(re_status) != 0:
        for status in re_status:
            if status.lower() == "off market":
                omarket_price_content = [content.find_all("div", {"class" : "d-flex justify-content-between bold600"}) for content in soup_property]
                omarket_price_content = [price if len(price) != 0 else ["-"] for price in omarket_price_content]
                omarket_price_pattern = '''<div class="mdText"><div>(.*?)<\/div><\/div><div class="xlText"><\/div><div class="mdText"><div>(.*?)<\/div>'''
                omarket_listing_price = [re.findall(omarket_price_pattern, str(price[0]), re.DOTALL) for price in omarket_price_content]
                omarket_listing_price = [price if len(price) != 0 else ["-"] for price in omarket_listing_price]
                omarket_listing_price = ["-".join(price[0]) for price in omarket_listing_price]
                return omarket_listing_price
            elif status.lower() == "for sale":
                sale_price_content = [content.find_all("span", {"class" : "lgText text-left PropertyInfo__propertyDisplayPrice--ZcRYj"}) for content in soup_property]
                sale_listing_price = [price[0].text if len(price) != 0 else "-" for price in sale_price_content]
                return sale_listing_price
            elif status.lower() == "for rent":
                rent_price_content = [content.find_all("span", {"class" : "lgText text-left PropertyInfo__propertyDisplayPrice--ZcRYj"}) for content in soup_property]
                rent_listing_price = [price[0].text if len(price) != 0 else "-" for price in rent_price_content]
                return rent_listing_price
            else:
                return "Error"
    else:
        return []
listing_price = get_price(property_status)

# print(property_status)
# print(street)
# print(suburb)
# print(floor_area)
# print(land_area)
# print(no_of_bds)
# print(no_of_baths)
# print(no_of_carspaces)
# print(year_built)
# print(building_type)
# print(listing_price)
# print(sold_time)
# print(sold_price)
# print(get_url())

print(len(property_status))
print(len(street))
print(len(suburb))
print(len(floor_area))
print(len(land_area))
print(len(no_of_bds))
print(len(no_of_baths))
print(len(no_of_carspaces))
print(len(year_built))
print(len(building_type))
print(len(listing_price))
print(len(sold_time))
print(len(sold_price))
print(len(get_url()))

# export into a csv file
data = {
    "Status" : property_status,
    "Street" : street,
    "Suburb" : suburb,
    "Floor Area" : floor_area, 
    "Land Area" : land_area,
    "# Of Rooms" : no_of_bds, 
    "Baths" : no_of_baths, 
    "Parking" : no_of_carspaces, 
    "Year Built" : year_built, 
    "Type" : building_type, 
    "Listing Price" : listing_price,
    "Sold Time" : sold_time,
    "Sold Price" : sold_price,
    "URL" : get_url()
}

headers = [
    "Status",
    "Street",
    "Suburb",
    "Floor Area", 
    "Land Area",
    "# Of Rooms", 
    "Baths", 
    "Parking", 
    "Year Built", 
    "Type", 
    "Listing Price",
    "Sold Time",
    "Sold Price",
    "URL"
    ]

df = pd.DataFrame(data, columns = headers)
df.to_csv("[Mel] off_market_19.csv", index = False)

