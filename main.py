import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# to do:
# find the cheapest place to buy each card
# find the cheapest place to buy the whole deck

# set up the selenium driver to get the html data from the site
options = Options()
options.add_argument("-headless")
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe' # may be device specific
script_file_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_file_path)
x_path = os.path.join(script_directory, "geckodriver.exe") # assumes geckodriver is in the same folder as the python file
service = Service(x_path)
driver = webdriver.Firefox(service=service,options=options)

# set up list to add stores to 
stores = {}
missing_cards = []

# set up list of cards to search for
deck_list = open(os.path.dirname(script_file_path) + "\decklist.txt","r")
deck_list = deck_list.read().split("\n")

# send an html query for a specific card
def search_card(card_name):
    # print(card_name)
    formatted_name = format_name(card_name)
    driver.get("https://www.mtgsingles.co.nz/card/" + formatted_name)
    time.sleep(1) # wait one second to not overload the site
    return driver.page_source

# format a card name so that it can be used in a url
def format_name(card_name):
    # make all characters lowercase and put them in an array
    card_name = card_name.lower()
    card_array = [char for char in card_name]
    # replace all spaces in the card name with %20
    for i in range(len(card_array)):
        if card_array[i] == " ":
            card_array[i] = "%20"
    return "".join(card_array)

# parse the html data to get the various prices, put them in a dictionary
def parse_html(card_name):
    html = search_card(card_name)
    # parse the html data to get the various prices, put them in a dictionary
    html_lines = html.split("\n")
    raw_data = html_lines[31] # this is the line that contains the card data
    raw_data = raw_data.split("<")
    site_data = []
    price_data = []
    name_data = []
    for line in raw_data:
        if "class=\"mtgCard nostyle\"" in line: # check for lines with store links
            site_data.append(line[70:-2])
        if "class=\"price\"" in line: # check for lines with prices
            price_data.append(line[42:])
        if "class=\"title\"" in line: # check for card name
            name_data.append(line[41:])
    if len(site_data) == 0: # if no printings are available, add the card to the missing card list
        missing_cards.append(card_name)
    scraped_stores = []
    for i in range(len(site_data)):
        # print(card_name)
        site_name = site_data[i].split("/")[2] # get the site name from the url
        if site_name not in stores:
            stores.update({site_name:{}}) # add the site to the dictionary of stores
        if site_name not in scraped_stores: # check the site doesn't already have an entry
            # add the card to the store's inventory
            # stores.get(site_name).update({card_name:float(price_data[i])})
            if " Art Card" not in name_data[i]: # remove art cards from any results
                stores.get(site_name)[card_name] = float(price_data[i])
                scraped_stores.append(site_name)
            # print(site_name + ": " + str(stores.get(site_name).get(card_name)))

def process_stores():
    output_file = open("cardlocations.txt","w")
    for store in stores.keys():
        print(store + ": " + str(len(stores.get(store).keys())) + " card(s) in stock")
        store_cost = 0
        output_file.write(store + " (" + str(len(stores.get(store).keys())) + " card(s))" + "\n")
        for card in stores.get(store).keys():
            output_file.write(card + ": $" + str(stores.get(store).get(card)) + "\n")
            store_cost += stores.get(store).get(card)
            # print(card + ": $" + str(stores.get(store).get(card)))
        output_file.write("Total cost: $" + str(round(store_cost,2)) + "\n\n")
    if len(missing_cards) > 0:
        print("Missing card(s): ")
        output_file.write("Missing card(s): \n")
        for card in missing_cards:
            print(card)
            output_file.write(card + "\n")
    output_file.close()

# process the list of cards
for card in range(len(deck_list)):
    # card = card.split("\n")[0]
    # print(deck_list[card])
    parse_html(deck_list[card])

process_stores()

# stuff below is just for testing the card search for a card with special characters
# name = "dovin's veto"
# name = format_name(name)
# sitedata = search_card(name)
# cardline = parse_html(sitedata,name)

driver.close()