from selenium import webdriver
import time
import re
import pandas as pd

# Setup Driver
options = webdriver.chrome.options.Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Where I will gather data from
host = 'https://www.mapdevelopers.com/distance_from_to.php'

# Pull in spreadsheet from excel into pandas
df = pd.read_excel('distances.xlsm', header=1)
# Drop population column
df = df.drop('Unnamed: 1', axis=1)
# Fix columns
df.columns = ['zip'] + list(df.columns[1:])
# Purge useless rows (non data)
df = df.drop(0)

# Origins and destinations from excel spreadsheet
origins = list(df['zip'])
destinations = list(df.columns)[1:] # [1:] to ignore the zip column

print(origins, destinations)
exit()

# Object holding all the data
data = {
    'origin': {
        'location' : 289,
        'location2' : 239
    }
}

# Loop through each origin and mark its connection to each destination
for origin in origins:
    for destination in destinations:
        # Process destination to replace all spaces with html safe characters
        destination = destination.replace(' ', '%20')
        # Get Data from website
        driver.get(host + f'?&from={origin}&to={destination}')
        distances = driver.find_element_by_id('driving_status')
        # Rest for a bit so that the update can occur
        time.sleep(1.5)
        # Pull out miles
        miles = re.search(r'\d*\.?\d+', distances.text).group()
        print(miles)
