from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import pandas as pd
from csv import DictWriter

data_file = input('Input name of data file e.g. distances.xlsm: ')
csv_file = input('Input name of output file e.g. data.csv: ')
start_from = input('Input row to start from starting with 0 index e.g. 0 for the first row or 2 for the third row: ')

# Setup Driver
options = webdriver.chrome.options.Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Where I will gather data from
host = 'https://www.mapdevelopers.com/distance_from_to.php'

# Pull in spreadsheet from excel into pandas
df = pd.read_excel(data_file, header=1)
# Drop population column
df = df.drop('Unnamed: 1', axis=1)
# Fix columns
df.columns = ['zipcode'] + list(df.columns[1:])
# Purge useless rows (non data)
df = df.drop(0)

# Origins and destinations from excel spreadsheet
origins = list(df['zipcode'])[start_from:] # Start_from
destinations = list(df.columns)[1:] # [1:] to ignore the zipcode column

# Get info from website
def get_data(origin, destination, depth=0):
    # Process destination to replace all spaces with html safe characters
    destination = destination.replace(' ', '%20')
    # Get Data from website
    driver.get(host + f'?&from={origin}&to={destination}')
    try:
        distances = driver.find_element_by_id('driving_status')
    except NoSuchElementException:
        # If any error is found in finding the element, just return 0.0
        return '0.0'
    # Rest for a bit so that the update can occur
    time.sleep(3)
    # Pull out miles
    miles = re.search(r'\d*\.?\d+', distances.text).group()
    # Ensure that you got the miles before returning it, if not try again, but only 3 tries
    if miles == '0.0' and depth < 3:
        return get_data(origin, destination, depth=depth+1)
    else:
        return miles

# Setup csv file
with open(csv_file, 'w+') as f:
    # Creat dictwriter
    writer = DictWriter(f, fieldnames=df.columns)
    # Write to file
    writer.writeheader()

# Saving function
def save_data(data, save_file):
    # Open csv file
    with open(save_file, 'a') as f:
        # Creat dictwriter
        writer = DictWriter(f, fieldnames=df.columns)
        # Write to file
        writer.writerow(data)

# Loop through each origin and mark its connection to each destination
for origin in origins:
    # Add origin to data set
    data = {'zipcode' : origin}
    for destination in destinations:
        # Add miles under destination label for origin
        print(f'Getting data for distance from {origin} to {destination}')
        data[destination] = get_data(origin, destination)
    # Make a backup csv of each origin every time you go through
    save_data(data, csv_file)