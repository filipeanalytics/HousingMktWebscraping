import time  # to use sleep function to allow website to load
from selenium import webdriver  # to connect to a browser and access an URL
from bs4 import BeautifulSoup  # to remove HTML tags from HTML content
from selenium.webdriver.common.keys import Keys  # so I can press the Enter Key in the search fields
import pandas as pd

# WEBSCRAPING PROPERTIES FOR SALE and RENTAL PROPERTIES from rew.ca
# By: Filipe Camara de Oliveira
# ALGORITHM
# 0 - Need to iterate to collect data from all regions, and all cities within each region
# 1 - for with the size of number of regions (13 or lengh(regionsSize) )
# 2 - each iteration wll have another for that will navigate through each region's city (regionsSize)
    # .gridblock-link   177 cities
# 3 - After clicking on city, store "# Listings" value as it will determine how many pages will need to be read.
# 4 - Click on "# Listings" to display all rental units in that city
# 5 - For loop with "# Listings" length.
    #  If read all results in a page and haven't reach the "# Listings", click load more and repeat process
    #  Otherwise finished collecting data for this city

class Property:
    price = ""
    address = ""
    neighborhood = ""  # e.g. East Van
    city = ""  # e.g. Vancouver
    region = ""  # e.g. Greater Vancouver
    bedrooms = ""
    bathrooms = ""
    area = ""
    propType = ""  # e.g. Apt/Condo, House, Townhouse

    def __init__(self, price, address, neighborhood, city,
                 region, bedrooms, bathrooms, area, propType):
        self.price = price
        self.address = address
        self.neighborhood = neighborhood
        self.city = city
        self.region = region
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.area = area
        self.propType = propType

    def showDetails(self):
        print("Price:       " + self.price)
        print("Address: " + self.address)
        print("Neighborhood:       " + self.neighborhood)
        print("City:  " + self.city)
        print("Region:      " + self.region)
        print("# Bedrooms:      " + self.bedrooms)
        print("# Bathrooms:    " + self.bathrooms)
        print("Area (sf):       " + self.area)
        print("Property type:       " + self.propType)
        print("")

def HTMLtoText(HTMLelement):
    textContent = HTMLelement.get_attribute('innerHTML')
    # Beautiful soup removes HTML tags from content, if it exists.
    soup = BeautifulSoup(textContent, features="lxml")
    rawString = soup.get_text().strip()  # Leading and trailing whitespaces are removed
    return rawString

#  Connect to Browser
DRIVER_PATH = "C:/Users/filip/Documents/PythonFiles/chromedriver"
browser = webdriver.Chrome(DRIVER_PATH)

# Can use same code for both Rent and Buy
URLbuy = "https://www.rew.ca/sitemap/real-estate/bc"
# URLrent = "https://www.rew.ca/sitemap/rentals/bc"

#  Access website
# browser.get(URLrent)
browser.get(URLbuy)
# Give the browser time to load all content.
time.sleep(2)

propertiesList = [] # will store all properties collected into a list of objects

# Create dataframe with named columns.
df = pd.DataFrame(columns=['price', 'address', 'neighborhood', 'city', 'region',
                           'bedrooms', 'bathrooms', 'area', 'propType'])


regions = browser.find_elements_by_css_selector(".gridblock header") # includes all 13 regions
citiesPerRegion = [5, 17, 8, 14, 15, 32, 5, 6, 46, 12, 8, 6, 3]  # number of cities in each region

cities = browser.find_elements_by_css_selector(".gridblock-link")  # includes all 177 cities
citiesCounter = 0 # This counter will control the city that is being read

regionsList = [] # will store all 13 region names

# Create dataframe with named columns to store every individual property details
df = pd.DataFrame(columns=['price', 'address', 'neighborhood', 'city', 'region',
                           'bedrooms', 'bathrooms', 'area', 'propType'])

# 1 - for with the size of number of regions (13 or lengh(regionsSize) ) len(regions)
for i in range(len(regions)): # navegates through each of the 13 regions
    regions = browser.find_elements_by_css_selector(".gridblock header")  # includes all 13 regions
    region = HTMLtoText(regions[i])
    regionsList.append(region)

    # 2 - each iteration wll have another for loop that will navigate through each region's city (citiesPerRegion)
    # .gridblock-link   177 cities
    for j in range(citiesPerRegion[i]):  # navegates through all cities in each region
        cities = browser.find_elements_by_css_selector(".gridblock-link")  # includes all 177 cities
        citySelector = cities[citiesCounter] # current city being read
        city = HTMLtoText(citySelector)

        citiesCounter = citiesCounter + 1  # This counter will control the city that is being read

        citySelector.send_keys(Keys.RETURN)  # clicking on city
        time.sleep(3)

        # 3 - After clicking on city, store "# Listings" value as it will determine how many pages will need to be read for that city.
        listingsSelector = browser.find_element_by_css_selector(".statsbanner a")  # "# Listings" link
        numberOfListings = HTMLtoText(listingsSelector)
        # Cleaning numberOfListings to have only numbers (remove "Listings" part)
        #  rfind(sub [,start [,end]])
        #  Return the highest index in the string where substring sub is found, such that sub is contained within s[start,end].
        indexLimit = numberOfListings.rfind(" ")
        numberOfListings = numberOfListings[:indexLimit]  # will get just the numeric part of "1234 Listings"
        numberOfListings = int(numberOfListings)

        if numberOfListings != 0:  # if there is any listings to be read

        #  4 - Click on "# Listings" to display all rental units in that city
            listingsSelector.send_keys(Keys.RETURN)  # clicking on "# Listings"
            time.sleep(1)

        # 5 - For loop with "# Listings" length.
            #  If read all results in a page and haven't reach the "# Listings", click load more and repeat process
            #  Otherwise finished collecting data for this city

            propCollected = 0  # will control total properties that were collected among all pages
            propertiesList = []  # list that will store all properties collected

            while propCollected < numberOfListings:  # while haven't read all listings for current city

                # propDetailsSelector will get all properties displayed on current page
                propPerPageSelector = browser.find_elements_by_css_selector(".displaypanel-content")
                numberPropOnPage = len(propPerPageSelector)  # number of properties on current page

                priceSelector = browser.find_elements_by_css_selector(".displaypanel-title")
                addressSelector = browser.find_elements_by_css_selector(".hidden-xs+ .displaypanel-section")
                propDetailsSelector = browser.find_elements_by_css_selector(".clearfix .l-pipedlist") # bd ba sf
                propTypeSelector = browser.find_elements_by_css_selector(".hidden-xs .displaypanel-info")
                neighborhoodSelector = browser.find_elements_by_css_selector(".displaypanel-info li:nth-child(1)")

                #  Read and store each property detail in propDetailsList.
                for j in range(numberPropOnPage):
                    # CONVERTING RESULTS TO TEXT
                    # price is duplicated, so will do jx2(index): 0x2(0) 1x2(2) 2x2(4)...6x2(12)
                    try: # was getting an error due to extra properties advertised
                        priceText = HTMLtoText(priceSelector[j*2])
                        addressText = HTMLtoText(addressSelector[j])
                        propDetailsText = HTMLtoText(propDetailsSelector[j])
                        propTypeText = HTMLtoText(propTypeSelector[j])
                        neighborhoodText = HTMLtoText(neighborhoodSelector[j])
                        if neighborhoodText == city:  # means there is no neighborhood
                            neighborhood = ""
                        else:
                            neighborhood = neighborhoodText
                    except Exception as e:
                        # print(e)  # list index out of range. 23 number of listings, but 22 properties. 1 is an ad.
                        pass  # do nothing

                    # CLEANING RESULTS
                    # price
                    startIndex = priceText.index('$')+1  # starts reading from this point
                    if priceText.find("/") == -1:  # if = -1, means haven't found it
                        cutOffIndex = len(priceText)
                    else:  # price has "/month" attached to it
                        cutOffIndex = priceText.index('/')  # cuts the string at /month
                    price = priceText[startIndex:cutOffIndex]

                    # address
                    try:
                        cutOffIndex = addressText.index('\n')  # cuts the string at \n
                        address = addressText[:cutOffIndex]
                    except Exception as e:
                        address = ""

                    # bd                                           # '2 bd\n2 ba\n936 sf'
                    bedrooms = propDetailsText.partition(' bd')[0] # '2' ' bd' '\n2 ba\n936 sf'
                    # ba
                    bathrooms = propDetailsText.partition(' ba')[0] # '2 bd\n2'  ' ba'   '\n936 sf'
                    bathrooms = bathrooms.partition('\n')[2] # '2 bd\n2' -> '2 bd'   '\n'   '2'
                    # sf
                    area = propDetailsText.rpartition('\n')[2] # '2 bd\n2 ba\n936 sf' -> '936 sf'
                    area = area.rpartition(' sf')[0] # '936 sf' -> '936'
                    # prop Type
                    propType = propTypeText

                    # STORING PROPERTY DETAILS INTO A LIST OF OBJECTS
                    # Creating property object
                    propertyObj = Property(price, address, neighborhood, city, region, bedrooms, bathrooms, area, propType)
                    # appending property by property into an Object's List.
                    propertiesList.append(propertyObj)

                    # STORING PROPERTY DETAILS INTO A DATAFRAME
                    # adding one property info into a dictionary
                    propDict = {'price': propertyObj.price, 'address': propertyObj.address,
                                  'neighborhood': propertyObj.neighborhood, 'city': propertyObj.city,
                                  'region': propertyObj.region, 'bedrooms': propertyObj.bedrooms,
                                  'bathrooms': propertyObj.bathrooms, 'area': propertyObj.area,
                                  'propType': propertyObj.propType}
                    # appending property by property into a DataFrame
                    df = df.append(propDict, ignore_index=True)

                propCollected = propCollected + numberPropOnPage

                # if there are more properties to be collected, load more results
                if propCollected < numberOfListings:
                    try:
                        loadMoreResults = browser.find_element_by_css_selector(".paginator-next_page a")
                        loadMoreResults.click()
                    except Exception as e:
                        # print(e)
                        propCollected = numberOfListings  # forces to end the for loop and get out of this city
                    time.sleep(2)

        # When finished reading all properties in one city, go back to main page
        # browser.get(URLrent)
        browser.get(URLbuy)
        # Give the browser time to load all content.
        time.sleep(2)
# print(propDetailsList)

# Save DataFrame into a CSV File
PATH = "C:/Users/filip/Documents/PythonFiles/"
CSV_FILE = "PropertiesOnSale.csv"
df.to_csv(PATH+CSV_FILE, sep=',')
